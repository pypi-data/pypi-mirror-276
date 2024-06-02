import torch

class UnivariateGaussianLikelihood():
    """
    The univariate Gaussian observation likelihood assumes that $y\sim\mathcal{N}(y\mid x; \mu,\sigma)$.
    The density of the Gaussian likelihood in the univariate case is
    $$
    p(y\mid x) = \\frac{1}{\sigma(x)\sqrt{2\pi}}\exp\left(-\\frac{1}{2}\left(\\frac{y-\mu(x)}{\sigma(x)}\\right)^2\\right).
    $$
    The support of the univariate Gaussian is $y\in\mathbb{R}$. Since this is the univariate case, the shape `Y` when calling `DKR.fit(X,Y)` needs to be `(n,1)`. For the multivariate case, see the [multivariate Gaussian Liklihood](observation_likelihoods.md#multivariate-observation-likelihoods).

    Args:
        mu_correction (str): Whether or not a correction of the expected mean should be carried out. When fitting a Gaussian distribution to data, the mean $\mu$ is calculated prior to the calculation of the standard deviation $\sigma$. Both $\mu$ and $\sigma$ are functions of $y$. In areas when $\mu$ rapidly changes, the estimated standard deviation $\sigma$ becomes inflated as the estimation for the standard deviation assume constant standard deviation across all $x$. Using `mu_prediction`, uses information about the already calculated $\mu$. Specifically, using `mu_correction`, $\\tilde{y}=y-(\mu(x)-\mu(x_q))$ will be used instead of $y$. `mu_prediction` can be chosen from three options: `always`, `predict`, or `never`. When `always` is selected, the correction will be carried out at every optimization step which is costly. `predict` doesn't run the correction when `DKR.fit` is called, but runs it when `DKR.predict` is called. This option represents a suitable balance between runtime and and model fidelity. Lastly, `\\never`, does not use the correction step during fitting or prediction.
        ) 

    Attributes:
        param_names (list): A list of strings that contains the names of the model parameters. For the univariate Gaussian likelihood, this is 'mu' and 'sigma'.
        mu_correction (str): Either 'always', 'predict', or 'never'. See above for a functional description of `mu_correction`.
    
    Examples:
        ```py
        import torch
        from dkregression.kernels import RBF
        from dkregression.likelihoods import UnivariateGaussianLikelihood
        from dkregression.cross_validation import CrossValidation
        from dkregression import DKR

        X = torch.rand((100,2))
        Y = torch.rand((100,1))

        kernel = RBF(X)
        likelihood = UnivariateGaussianLikelihood()
        cv = CrossValidation()

        model = DKR(kernel, likelihood, cv)
        model.fit(X,Y)
        ```
    
    """
    def __init__(self,mu_correction="predict") -> None:
        self.param_names = ["mu", "sigma"]
        self.mu_correction = mu_correction

    def compute_params(self,k:torch.Tensor,x:torch.Tensor,y:torch.Tensor,kernel,eps:float=1e-12,eval=False):
        #k.shape = (nq,n)
        #y.shape = (n,1)
        # params is a dictionary with the keys "mu" and "sigma"
        #THIS VERSION ASSUMES THAT k IS NORMALIZED
        params = {}
        params["mu"] = torch.sum(k*y.T,dim=-1,keepdim=True)
        if self.mu_correction=="always" or (self.mu_correction=="predict" and eval):
            mu_x = torch.sum(kernel.kernel_matrix(x,x)*y.T,dim=-1,keepdim=True).unsqueeze(0)
            mu_xq = params["mu"].unsqueeze(1)
            y_corrected = (y.unsqueeze(0)-(mu_x-mu_xq)).squeeze()
            params["sigma"] = torch.sqrt(torch.maximum(params["mu"]**2 + torch.sum(k*y_corrected**2,dim=-1,keepdim=True) - 2*params["mu"]*torch.sum(k*y_corrected,dim=-1,keepdim=True),torch.zeros_like(params["mu"],dtype=torch.float64)))+ eps
        else:
            params["sigma"] = torch.sqrt(torch.maximum(-params["mu"]**2 + torch.sum(k*(y.T)**2,dim=-1,keepdim=True),torch.zeros_like(params["mu"],dtype=torch.float64))) + eps   #maximum to avoid issues with nans due to numerical issues

        return params
    
    def evaluate_log_likelihood(self,yq,params):
        #each entry in params must have the same shape as yq
        for key in params:
            p = params[key]
            assert p.shape == yq.shape
        
        log_probs = torch.distributions.normal.Normal(params["mu"],params["sigma"]).log_prob(yq)

        return log_probs
    