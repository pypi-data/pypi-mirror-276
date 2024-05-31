from typing import List, Optional, Sequence, Literal, Union

import numpy as np
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
import hmivae
from hmivae._hmivae_base_components import DecoderHMIVAE, EncoderHMIVAE
from pytorch_lightning.callbacks import Callback

# from anndata import AnnData

torch.backends.cudnn.benchmark = True


class hmiVAE(pl.LightningModule):
    """
    Variational Autoencoder for hmiVAE based on pytorch-lightning.
    """

    def __init__(
        self,
        input_exp_dim: int,
        input_corr_dim: int,
        input_morph_dim: int,
        input_spcont_dim: int,
        E_me: int = 32,
        E_cr: int = 32,
        E_mr: int = 32,
        E_sc: int = 32,
        E_cov: int = 10,
        latent_dim: int = 10,
        n_covariates: int = 0,
        leave_out_view: Optional[Union[None, Literal['expression', 'correlation', 'morphology', 'spatial']]] = None,
        use_covs: bool = False,
        use_weights: bool = True,
        n_hidden: int = 1,
        beta_scheme: Optional[Literal['constant', 'warmup']] = 'warmup',
        batch_correct: bool = True,
        n_steps_kl_warmup: Union[int, None] = None,
        n_epochs_kl_warmup: Union[int, None] = 10,
    ):
        super().__init__()
        self.n_steps_kl_warmup = n_steps_kl_warmup
        self.n_epochs_kl_warmup = n_epochs_kl_warmup
        self.n_covariates = n_covariates

        self.batch_correct = batch_correct

        self.use_covs = use_covs

        self.use_weights = use_weights

        self.leave_out_view = leave_out_view

        self.beta_scheme = beta_scheme

        self.encoder = EncoderHMIVAE(
            input_exp_dim,
            input_corr_dim,
            input_morph_dim,
            input_spcont_dim,
            E_me,
            E_cr,
            E_mr,
            E_sc,
            latent_dim,
            E_cov=E_cov,
            n_covariates=n_covariates,
            leave_out_view=leave_out_view,
            n_hidden=n_hidden,
        )

        self.decoder = DecoderHMIVAE(
            latent_dim,
            E_me,
            E_cr,
            E_mr,
            E_sc,
            input_exp_dim,
            input_corr_dim,
            input_morph_dim,
            input_spcont_dim,
            E_cov=E_cov,
            n_covariates=n_covariates,
            leave_out_view=leave_out_view,
            n_hidden=n_hidden,
        )

        self.save_hyperparameters(ignore=["adata"])

    def reparameterization(self, mu, log_std):
        std = torch.exp(log_std)
        eps = torch.randn_like(log_std)

        # sampling from encoded distribution
        z_samples = mu + eps * std

        return z_samples

    def KL_div(self, enc_x_mu, enc_x_logstd, z):
        """Takes in the encoded x mu and sigma, and the z sampled from
        q, and outputs the KL-Divergence term in ELBO"""

        p = torch.distributions.Normal(
            torch.zeros_like(enc_x_mu), torch.ones_like(enc_x_logstd)
        )
        enc_x_std = torch.exp(enc_x_logstd)
        q = torch.distributions.Normal(enc_x_mu, enc_x_std + 1e-6)

        log_q_zx = q.log_prob(z)
        log_p_z = p.log_prob(z)

        kl = log_q_zx - log_p_z
        kl = kl.sum(-1)

        return kl

    def compute_kl_weight(
        self,
        epoch: int,
        step: Optional[int],
        n_epochs_kl_warmup: Optional[int],
        n_steps_kl_warmup: Optional[int],
        max_kl_weight: float = 1.0,
        min_kl_weight: float = 0.0,
    ) -> float:
        """
        Compute the weight for the KL-Div term in loss.
        Taken from scVI:
        https://github.com/scverse/scvi-tools/blob/2c22bda9bcfb5a89d62c96c4ad39d8a1e297eb08/scvi/train/_trainingplans.py#L31
        """
        slope = max_kl_weight - min_kl_weight

        if min_kl_weight > max_kl_weight:
            raise ValueError(
        f"min_kl_weight={min_kl_weight} is larger than max_kl_weight={max_kl_weight}"
        )

        if n_epochs_kl_warmup:
            if epoch < n_epochs_kl_warmup:
                return slope * (epoch / n_epochs_kl_warmup) + min_kl_weight
        elif n_steps_kl_warmup:
            if step < n_steps_kl_warmup:
                return slope * (step / n_steps_kl_warmup) + min_kl_weight

        return max_kl_weight


    def em_recon_loss(
        self,
        dec_x_mu_exp,
        dec_x_logstd_exp,
        dec_x_mu_corr,
        dec_x_logstd_corr,
        dec_x_mu_morph,
        dec_x_logstd_morph,
        dec_x_mu_spcont,
        dec_x_logstd_spcont,
        y,
        s,
        m,
        c,
        weights: Optional[Union[None, torch.Tensor]]=None,
    ):
        """Takes in the parameters output from the decoder,
        and the original input x, and gives the reconstruction
        loss term in ELBO
        dec_x_mu_exp: torch.Tensor, decoded means for protein expression feature
        dec_x_logstd_exp: torch.Tensor, decoded log std for protein expression feature
        dec_x_mu_corr: torch.Tensor, decoded means for correlation feature
        dec_x_logstd_corr: torch.Tensor, decoded log std for correlations feature
        dec_x_mu_morph: torch.Tensor, decoded means for morphology feature
        dec_x_logstd_morph: torch.Tensor, decoded log std for morphology feature
        dec_x_mu_spcont: torch.Tensor, decoded means for spatial context feature
        dec_x_logstd_spcont: torch.Tensor, decoded log std for spatial context feature
        y: torch.Tensor, original mean expression input
        s: torch.Tensor, original correlation input
        m: torch.Tensor, original morphology input
        c: torch.Tensor, original cell context input
        weights: torch.Tensor, weights calculated from decoded means for protein expression feature
        """

        ## Mean expression
        dec_x_std_exp = torch.exp(dec_x_logstd_exp)
        p_rec_exp = torch.distributions.Normal(dec_x_mu_exp, dec_x_std_exp + 1e-6)
        log_p_xz_exp = p_rec_exp.log_prob(y)
        log_p_xz_exp = log_p_xz_exp.sum(-1)

        
        ## Correlations
        dec_x_std_corr = torch.exp(dec_x_logstd_corr)
        p_rec_corr = torch.distributions.Normal(dec_x_mu_corr, dec_x_std_corr + 1e-6)
        if weights is None:
            log_p_xz_corr = p_rec_corr.log_prob(s)
        else:
            log_p_xz_corr = torch.mul(
                weights, p_rec_corr.log_prob(s)
            )  # does element-wise multiplication
        log_p_xz_corr = log_p_xz_corr.sum(-1)

        
        ## Morphology
        dec_x_std_morph = torch.exp(dec_x_logstd_morph)
        p_rec_morph = torch.distributions.Normal(dec_x_mu_morph, dec_x_std_morph + 1e-6)
        log_p_xz_morph = p_rec_morph.log_prob(m)
        log_p_xz_morph = log_p_xz_morph.sum(-1)

        
        ## Spatial context
        dec_x_std_spcont = torch.exp(dec_x_logstd_spcont)
        p_rec_spcont = torch.distributions.Normal(
            dec_x_mu_spcont, dec_x_std_spcont + 1e-6
        )
        log_p_xz_spcont = p_rec_spcont.log_prob(c)  # already dense matrix
        log_p_xz_spcont = log_p_xz_spcont.sum(-1)



        return (
            log_p_xz_exp,
            log_p_xz_corr,
            log_p_xz_morph,
            log_p_xz_spcont,
        )

    def neg_ELBO(
        self,
        enc_x_mu,
        enc_x_logstd,
        dec_x_mu_exp,
        dec_x_logstd_exp,
        dec_x_mu_corr,
        dec_x_logstd_corr,
        dec_x_mu_morph,
        dec_x_logstd_morph,
        dec_x_mu_spcont,
        dec_x_logstd_spcont,
        z,
        y,
        s,
        m,
        c,
        weights:Optional[Union[None, torch.Tensor]]=None,
    ):
        kl_div = self.KL_div(enc_x_mu, enc_x_logstd, z)

        (
            recon_lik_me,
            recon_lik_corr,
            recon_lik_mor,
            recon_lik_sc,
        ) = self.em_recon_loss(
            dec_x_mu_exp,
            dec_x_logstd_exp,
            dec_x_mu_corr,
            dec_x_logstd_corr,
            dec_x_mu_morph,
            dec_x_logstd_morph,
            dec_x_mu_spcont,
            dec_x_logstd_spcont,
            y,
            s,
            m,
            c,
            weights,
        )
        return (
            kl_div,
            recon_lik_me,
            recon_lik_corr,
            recon_lik_mor,
            recon_lik_sc,
        )


    def loss(self, kl_div, recon_loss, beta: float = 1.0):

        return beta * kl_div.mean() - recon_loss.mean()

    def training_step(
        self,
        train_batch,
        recon_weights=np.array([1.0, 1.0, 1.0, 1.0]),
    ):
        """
        Carries out the training step.
        train_batch: torch.Tensor. Training data,
        spatial_context: torch.Tensor. Matrix with old mu_z integrated neighbours information,
        corr_weights: numpy.array. Array with weights for the correlations for each cell.
        recon_weights: numpy.array. Array with weights for each view during loss calculation.
        beta: float. Coefficient for KL-Divergence term in ELBO.
        """

        Y = train_batch[0]
        S = train_batch[1]
        M = train_batch[2]
        spatial_context = train_batch[3]
        if self.use_weights:
            weights = train_batch[5]
        else:
            weights = None

        if self.use_covs:
            categories = train_batch[6]
        else:
            categories = torch.Tensor([]).type_as(Y)

        if self.batch_correct:
            one_hot = train_batch[4]

            cov_list = torch.cat([one_hot, categories], 1).float().type_as(Y)
        elif self.use_covs:
            cov_list = categories
        else:
            cov_list = torch.Tensor([]).type_as(Y)

        mu_z, log_std_z = self.encoder(Y, S, M, spatial_context, cov_list)

        z_samples = self.reparameterization(mu_z, log_std_z)

        # decoding
        (
            mu_x_exp_hat,
            log_std_x_exp_hat,
            mu_x_corr_hat,
            log_std_x_corr_hat,
            mu_x_morph_hat,
            log_std_x_morph_hat,
            mu_x_spcont_hat,
            log_std_x_spcont_hat,
        ) = self.decoder(z_samples, cov_list)

        (
            kl_div,
            recon_lik_me,
            recon_lik_corr,
            recon_lik_mor,
            recon_lik_sc,
        ) = self.neg_ELBO(
            mu_z,
            log_std_z,
            mu_x_exp_hat,
            log_std_x_exp_hat,
            mu_x_corr_hat,
            log_std_x_corr_hat,
            mu_x_morph_hat,
            log_std_x_morph_hat,
            mu_x_spcont_hat,
            log_std_x_spcont_hat,
            z_samples,
            Y,
            S,
            M,
            spatial_context,
            weights,
        )

        if self.beta_scheme == 'warmup':

            beta = self.compute_kl_weight(
                self.current_epoch, 
                self.global_step,
                self.n_epochs_kl_warmup,
                self.n_steps_kl_warmup,
                )
        else:
            beta = 1.0

        if self.leave_out_view is not None:
            if self.leave_out_view == "expression":
                recon_weights = np.array([0.0, 1.0, 1.0, 1.0])
            if self.leave_out_view == "correlation":
                recon_weights = np.array([1.0, 0.0, 1.0, 1.0])
            if self.leave_out_view == "morphology":
                recon_weights = np.array([1.0, 1.0, 0.0, 1.0])
            if self.leave_out_view == 'spatial':
                recon_weights = np.array([1.0, 1.0, 1.0, 0.0])
        else:
            recon_weights=np.array([1.0, 1.0, 1.0, 1.0])

        recon_loss = (
            recon_weights[0] * recon_lik_me
            + recon_weights[1] * recon_lik_corr
            + recon_weights[2] * recon_lik_mor
            + recon_weights[3] * recon_lik_sc
        )

        loss = self.loss(kl_div, recon_loss, beta=beta)

        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
        self.log("beta", beta, on_step=True, on_epoch=True, prog_bar=False)
        self.log(
            "kl_div", kl_div.mean().item(), on_step=True, on_epoch=True, prog_bar=False
        )
        self.log(
            "recon_lik",
            recon_loss.mean().item(),
            on_step=True,
            on_epoch=True,
            prog_bar=False,
        )
        self.log(
            "recon_lik_me",
            recon_lik_me.mean().item(),
            on_step=True,
            on_epoch=True,
            prog_bar=False,
        )
        self.log(
            "recon_lik_corr",
            recon_lik_corr.mean().item(),
            on_step=True,
            on_epoch=True,
            prog_bar=False,
        )
        self.log(
            "recon_lik_mor",
            recon_lik_mor.mean().item(),
            on_step=True,
            on_epoch=True,
            prog_bar=False,
        )
        self.log(
            "recon_lik_sc",
            recon_lik_sc.mean().item(),
            on_step=True,
            on_epoch=True,
            prog_bar=False,
        )

        return {
            "loss": loss,
            "kl_div": kl_div.mean().item(),
            "recon_lik": recon_loss.mean().item(),
            "recon_lik_me": recon_lik_me.mean().item(),
            "recon_lik_corr": recon_lik_corr.mean().item(),
            "recon_lik_mor": recon_lik_mor.mean().item(),
            "recon_lik_sc": recon_lik_sc.mean().item(),
        }

    def validation_step(
        self,
        test_batch,
        n_other_cat: int = 0,
        L_iter: int = 300,
    ):
        """---> Add random one-hot encoding
        Carries out the validation/test step.
        test_batch: torch.Tensor. Validation/test data,
        spatial_context: torch.Tensor. Matrix with old mu_z integrated neighbours information,
        corr_weights: numpy.array. Array with weights for the correlations for each cell.
        recon_weights: numpy.array. Array with weights for each view during loss calculation.
        beta: float. Coefficient for KL-Divergence term in ELBO.
        """
        Y = test_batch[0]
        S = test_batch[1]
        M = test_batch[2]
        spatial_context = test_batch[3]
        batch_idx = test_batch[-1]
        
        if self.use_weights:
            weights = test_batch[5]
        else:
            weights = None

        if self.use_covs:
            categories = test_batch[6]
            n_classes = self.n_covariates - categories.shape[1]
        else:
            categories = torch.Tensor([]).type_as(Y)
            n_classes = self.n_covariates

        test_loss = torch.empty(size=[len(batch_idx), n_classes])
        elbo_full = torch.empty(size=[len(batch_idx), n_classes])

        for i in range(n_classes):

            if self.batch_correct:
                one_hot_zeros = torch.zeros(size=[1, n_classes])

                one_hot_zeros[0,i] = 1.0

                one_hot = one_hot_zeros.repeat((len(batch_idx),1)).type_as(Y)


                cov_list = torch.cat([one_hot, categories], 1).float().type_as(Y)
            elif self.use_covs:
                cov_list = categories
            else:
                cov_list = torch.Tensor([]).type_as(Y)

            mu_z, log_std_z = self.encoder(
                Y, S, M, spatial_context, cov_list
            )  # valid step

            z_samples = self.reparameterization(mu_z, log_std_z)

            # decoding
            (
                mu_x_exp_hat,
                log_std_x_exp_hat,
                mu_x_corr_hat,
                log_std_x_corr_hat,
                mu_x_morph_hat,
                log_std_x_morph_hat,
                mu_x_spcont_hat,
                log_std_x_spcont_hat,
            ) = self.decoder(z_samples, cov_list)

            (
                kl_div,
                recon_lik_me,
                recon_lik_corr,
                recon_lik_mor,
                recon_lik_sc,
            ) = self.neg_ELBO(
                mu_z,
                log_std_z,
                mu_x_exp_hat,
                log_std_x_exp_hat,
                mu_x_corr_hat,
                log_std_x_corr_hat,
                mu_x_morph_hat,
                log_std_x_morph_hat,
                mu_x_spcont_hat,
                log_std_x_spcont_hat,
                z_samples,
                Y,
                S,
                M,
                spatial_context,
                weights,
            )

            if self.beta_scheme == 'warmup':

                beta = self.compute_kl_weight(
                    self.current_epoch, 
                    self.global_step,
                    self.n_epochs_kl_warmup,
                    self.n_steps_kl_warmup,
                    )
            else:
                beta = 1.0

            if self.leave_out_view is not None:
                if self.leave_out_view == "expression":
                    recon_weights = np.array([0.0, 1.0, 1.0, 1.0])
                if self.leave_out_view == "correlation":
                    recon_weights = np.array([1.0, 0.0, 1.0, 1.0])
                if self.leave_out_view == "morphology":
                    recon_weights = np.array([1.0, 1.0, 0.0, 1.0])
                if self.leave_out_view == 'spatial':
                    recon_weights = np.array([1.0, 1.0, 1.0, 0.0])
            else:
                recon_weights=np.array([1.0, 1.0, 1.0, 1.0])

            recon_loss = (
                recon_weights[0] * recon_lik_me
                + recon_weights[1] * recon_lik_corr
                + recon_weights[2] * recon_lik_mor
                + recon_weights[3] * recon_lik_sc
            )


            loss = self.loss(kl_div, recon_loss, beta=beta)

            full_elbo = recon_loss.mean()-kl_div.mean()

            test_loss[:,i] = loss

            elbo_full[:,i] = full_elbo

        self.log(
            "test_loss",
            test_loss.mean(1).mean(),
            on_step=True,
            on_epoch=True,
            prog_bar=True,
        )  # log the average test loss over all the iterations
        self.log(
            "test_full_elbo", 
            elbo_full.mean(1).mean(),
            on_step=True,
            on_epoch=True,
            prog_bar=False,
            )
        self.log(
            "kl_div_test", kl_div.mean().item(), on_step=True, on_epoch=True, prog_bar=False
        )
        self.log("beta_test", beta, on_step=True, on_epoch=True, prog_bar=False)
        self.log(
            "recon_lik_test",
            recon_loss.mean().item(),
            on_step=True,
            on_epoch=True,
            prog_bar=False,
        )
        self.log(
            "recon_lik_me_test",
            recon_lik_me.mean().item(),
            on_step=True,
            on_epoch=True,
            prog_bar=False,
        )
        self.log(
            "recon_lik_corr_test",
            recon_lik_corr.mean().item(),
            on_step=True,
            on_epoch=True,
            prog_bar=False,
        )
        self.log(
            "recon_lik_mor_test",
            recon_lik_mor.mean().item(),
            on_step=True,
            on_epoch=True,
            prog_bar=False,
        )
        self.log(
            "recon_lik_sc_test",
            recon_lik_sc.mean().item(),
            on_step=True,
            on_epoch=True,
            prog_bar=False,
        )

        return {
            "loss": test_loss.mean(1).mean(),
            "kl_div": kl_div.mean().item(),
            "recon_lik": recon_loss.mean().item(),
            "recon_lik_me": recon_lik_me.mean().item(),
            "recon_lik_corr": recon_lik_corr.mean().item(),
            "recon_lik_mor": recon_lik_mor.mean().item(),
            "recon_lik_sc": recon_lik_sc.mean().item(),
        }

    def configure_optimizers(self):
        """Optimizer"""
        parameters = list(self.encoder.parameters()) + list(self.decoder.parameters())
        optimizer = torch.optim.Adam(parameters, lr=1e-3)
        return optimizer

    @torch.no_grad()
    def get_input_embeddings(
        self, x_mean, x_correlations, x_morphology, x_spatial_context
    ):
        """
        Returns the view-specific embeddings.
        """
        h_mean = F.elu(self.encoder.input_exp(x_mean))
        h_mean2 = F.elu(self.encoder.exp_hidden(h_mean))

        h_correlations = F.elu(self.encoder.input_corr(x_correlations))
        h_correlations2 = F.elu(self.encoder.corr_hidden(h_correlations))

        h_morphology = F.elu(self.encoder.input_morph(x_morphology))
        h_morphology2 = F.elu(self.encoder.morph_hidden(h_morphology))

        h_spatial_context = F.elu(self.encoder.input_spatial_context(x_spatial_context))
        h_spatial_context2 = F.elu(self.encoder.spatial_context_hidden(h_spatial_context))

        return h_mean2, h_correlations2, h_morphology2, h_spatial_context2

    @torch.no_grad()
    def inference(
        self,
        data,
        n_covariates: int,
        use_covs: bool = True,
        batch_correct: bool = True,
        indices: Optional[Sequence[int]] = None,
        give_mean: bool = True,
        view_specific_embeddings: Optional[bool] = True,
    ) -> np.ndarray:
        """
        Return the latent representation of each cell.
        """
        Y = data.Y
        S = data.S
        M = data.M
        C = data.C
        if use_covs:
            categories = data.BKG
            n_classes = n_covariates - categories.shape[1]
        else:
            categories = torch.Tensor([]).type_as(Y)
            n_classes = n_covariates

        if batch_correct:
            one_hot = self.random_one_hot(
                    n_classes=n_classes, n_samples=Y.shape[0]
                ).type_as(Y)

            cov_list = torch.cat([one_hot, categories], 1).float()
        else:
            cov_list = torch.Tensor([])

        if give_mean:
            mu_z, _ = self.encoder(Y, S, M, C, cov_list)

            if view_specific_embeddings:
                exp_e, corr_e, morph_e, spatial_e = self.get_input_embeddings(Y, S, M, C)

                return mu_z.numpy(), exp_e.numpy(), corr_e.numpy(), morph_e.numpy(), spatial_e.numpy()

            else:

                return mu_z.numpy()
        else:
            mu_z, log_std_z = self.encoder(Y, S, M, C, cov_list)

            z = self.reparameterization(mu_z, log_std_z)

            if view_specific_embeddings:
                exp_e, corr_e, morph_e, spatial_e = self.get_input_embeddings(Y, S, M, C)

                return z.numpy(), exp_e.numpy(), corr_e.numpy(), morph_e.numpy(), spatial_e.numpy()

            else:

                return z.numpy()

    @torch.no_grad()
    def random_one_hot(self, n_classes: int, n_samples: int):
        """
        Generates a random one hot encoded matrix.
        From:  https://stackoverflow.com/questions/45093615/random-one-hot-matrix-in-numpy
        """
        return torch.Tensor(np.eye(n_classes)[np.random.choice(n_classes, n_samples)])
