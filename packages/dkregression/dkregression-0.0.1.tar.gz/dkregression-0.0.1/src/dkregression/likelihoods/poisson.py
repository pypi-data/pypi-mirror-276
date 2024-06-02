import torch

class PoissonLikelihood():
    """
    The Poisson observation likelihood assumes that $y\sim\mathrm{Pois}(y\mid x; \lambda)$. The support of the Poisson distriubtion is only the non-negative integers $y\in\mathbb{N}_0$. Therefore, the method `DKR.fit(X,Y)` expects `Y` to be of the shape `(n,1)` when configured with the `PoissonLikelihood` and all values in `Y` to be non-negative integers. The probability mass is given by
    $$
    p(y\mid x) = \\frac{\lambda^y\exp (-\lambda)}{y!}.
    $$
    
    Attributes:
        param_names (list): A list of strings that contains the names of the model parameters. For the Poisson likelihood, the list contains 'lambda' as entry. This list is static and corresponds to keys of the dictionary returned by the `DKR.predict` method.
    
    Examples:
        ```py
        import torch
        from dkregression.kernels import RBF
        from dkregression.likelihoods import PoissonLikelihood
        from dkregression.cross_validation import CrossValidation
        from dkregression import DKR

        X = torch.rand((100,2))
        # the support of the Poisson distribution is only non-negative integers
        Y = torch.randint(0,20,(100,1))

        kernel = RBF(X)
        likelihood = PoissonLikelihood()
        cv = CrossValidation()

        model = DKR(kernel, likelihood, cv)
        model.fit(X,Y)
        ```
    """
    def __init__(self) -> None:
        self.param_names = ["lambda"]

    def compute_params(self,k,x,y,kernel,eval=False):
        #k.shape = (nq,n)
        #y.shape = (n,1)
        # params is a dictionary with the keys "lambda"
        #THIS VERSION ASSUMES THAT k IS NORMALIZED
        params = {}
        params["lambda"] = torch.sum(k*y.T,dim=-1,keepdim=True)

        return params

    def evaluate_log_likelihood(self,yq,params):
        for key in params:
            p = params[key]
            assert p.shape == yq.shape
        
        log_probs = torch.distributions.poisson.Poisson(params["lambda"]).log_prob(yq)

        return log_probs