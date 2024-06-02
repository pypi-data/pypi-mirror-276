import torch

class BernoulliLikelihood():
    """
    The Poisson observation likelihood assumes that $y\sim\mathrm{Ber}(y\mid x; p)$. The support of the Bernoulli distriubtion is only the binary set, so $y\in\{0,1\}$. Therefore, the method `DKR.fit(X,Y)` expects `Y` to be of the shape `(n,1)` when configured with the `BernoulliLikelihood` and only contain the values $0$ and $1$. The probability mass is given by
    $$
    p(y\mid x) = \\begin{cases}p(x) & \mathrm{for}~y=1 \\\\\\
            1-p(x) & \mathrm{for}~y=0~. \end{cases}
    $$
    
    Attributes:
        param_names (list): A list of strings that contains the names of the model parameters. For the Bernoulli likelihood, the list contains 'p' as entry. This list is static and corresponds to keys of the dictionary returned by the `DKR.predict` method.
    
    Examples:
        ```py
        import torch
        from dkregression.kernels import RBF
        from dkregression.likelihoods import BernoulliLikelihood
        from dkregression.cross_validation import CrossValidation
        from dkregression import DKR

        X = torch.rand((100,2))
        # the support of the Bernoulli distribution is the set of {0,1}
        Y = torch.randint(0,2,(100,1))

        kernel = RBF(X)
        likelihood = BernoulliLikelihood()
        cv = CrossValidation()

        model = DKR(kernel, likelihood, cv)
        model.fit(X,Y)
        ```
    """
    def __init__(self) -> None:
        self.param_names = ["p"]
    
    def compute_params(self,k,x,y,kernel,eps=1e-12,eval=False):
        params = {}
        params["p"] = torch.clamp(torch.sum(k*y.T,dim=-1,keepdim=True),eps,1-eps)   #avoid issues with interval during log-likelihood estimation
        
        return params
    
    def evaluate_log_likelihood(self,yq,params):
        for key in params:
            p = params[key]
            assert p.shape == yq.shape
            
        log_probs = torch.distributions.bernoulli.Bernoulli(params["p"]).log_prob(yq)
        
        return log_probs