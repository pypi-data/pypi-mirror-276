import torch
import nevergrad as ng

class DKR():
    def __init__(self,kernel,likelihood,cross_validation) -> None:
        self.kernel = kernel
        self.likelihood = likelihood
        self.cv = cross_validation
        self.x = None
        self.y = None
    
    def _update_kernel_params(self,params):
        assert params.keys() == self.kernel.params.keys()
        assert self.x is not None

        self.kernel.params = params

    def _neg_ll_cross_validation(self):
        assert self.x is not None
        assert self.y is not None

        dataset = self.cv.split_data(self.x,self.y)

        log_prob = self.cv.evaluate_likelihood(dataset,self.kernel,self.likelihood)
        return -log_prob.item()

    def _set_kernel_params_and_neg_ll(self,params):
        self._update_kernel_params(params)
        neg_ll = self._neg_ll_cross_validation()

        return neg_ll
    
    def fit(self,x,y,verbose=0,budget=100):
        self.x = x
        self.y = y

        param = ng.p.Dict(**{p:ng.p.Scalar(lower=self.kernel.params_lower_bound[p] ,upper=self.kernel.params_upper_bound[p]) for p in self.kernel.params})
        optimizer = ng.optimizers.NGOpt(parametrization=param, budget=budget)
        recommendation = optimizer.minimize(self._set_kernel_params_and_neg_ll,verbosity=verbose)

        #set optimal kernel parameters
        optimal_kernel_params = {p:recommendation[p].value for p in recommendation}
        self._update_kernel_params(optimal_kernel_params)

    def predict(self,xq):
        assert self.x is not None
        assert self.y is not None

        k = self.kernel.kernel_matrix(self.x,xq)
        likelihood_params = self.likelihood.compute_params(k,self.x,self.y,self.kernel,eval=True)

        return likelihood_params
