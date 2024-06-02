import torch

class MultivariateGaussianLikelihood():
    def __init__(self,mu_correction="predict",diagonal=False) -> None:
        self.param_names = ["mu", "sigma"]
        self.mu_correction = mu_correction
        self.diagonal = diagonal

    def compute_params(self,k,x,y,kernel,eps=1e-12,eval=False):
        #k.shape = (nq,n)
        #y.shape = (n,d)
        # params is a dictionary with the keys "mu" and "sigma"
        #THIS VERSION ASSUMES THAT k IS NORMALIZED
        D = y.shape[1]
        M = k.shape[0]

        assert D >= 2

        params = {}
        params["mu"] = torch.sum((k.unsqueeze(-1))*(y.unsqueeze(0)),dim=1)
        if self.mu_correction=="always" or (self.mu_correction=="predict" and eval):
            mu_x = torch.sum((kernel.kernel_matrix(x,x).unsqueeze(-1))*(y.unsqueeze(0)),dim=1).unsqueeze(0)
            # mu_x = torch.sum(kernel.kernel_matrix(x,x)*y.T,dim=-1,keepdim=True).unsqueeze(0)
            mu_xq = params["mu"].unsqueeze(1)
            y_corrected = (y.unsqueeze(0)-(mu_x-mu_xq)).squeeze()   #shape (M,N,D)   will break for D<2
            y_corrected_expanded = y_corrected.unsqueeze(-1)        #shpae (M,N,D,1)
            k_expanded = k.unsqueeze(-1).unsqueeze(-1)  #k is (M,N), need (M,N,1,1)
            mu_expanded = params["mu"].unsqueeze(1).unsqueeze(-1) #mu is (M,D), need (M,1,D,1)
            ymmu = y_corrected_expanded-mu_expanded #need shape (M,N,D,1)
            batch_outer_product = ymmu * torch.permute(ymmu,[0,1,3,2])   # (y-mu)(y-mu)^T
            params["sigma"] = torch.sum(k_expanded * batch_outer_product,dim=1) + eps*torch.eye(D).unsqueeze(0).repeat(M,1,1)
            
            # in the case of independnt variables
            if self.diagonal:
                diag_elements = torch.diagonal(params["sigma"],dim1=-2,dim2=-1)
                params["sigma"] = torch.diag_embed(diag_elements)

        else:
            k_expanded = k.unsqueeze(-1).unsqueeze(-1)  #k is (M,N), need (M,N,1,1)
            y_expanded = y.unsqueeze(0).unsqueeze(-1)     #y is (N,D), need (1,N,D,1)
            mu_expanded = params["mu"].unsqueeze(1).unsqueeze(-1) #mu is (M,D), need (M,1,D,1)
            ymmu = y_expanded-mu_expanded #need shape (M,N,D,1)
            # batch_outer_product = torch.einsum('abjk,abkl->abjl',ymmu,torch.permute(ymmu,[0,1,3,2]))    # (y-mu)(y-mu)^T
            batch_outer_product = ymmu * torch.permute(ymmu,[0,1,3,2])   # (y-mu)(y-mu)^T
            params["sigma"] = torch.sum(k_expanded * batch_outer_product,dim=1) + eps*torch.eye(D).unsqueeze(0).repeat(M,1,1)   #maximum to avoid issues with nans due to numerical issues also need to use maximum(0,other stuff)

            # in the case of independnt variables
            if self.diagonal:
                diag_elements = torch.diagonal(params["sigma"],dim1=-2,dim2=-1)
                params["sigma"] = torch.diag_embed(diag_elements)
                
        return params
    
    def evaluate_log_likelihood(self,yq,params):
        #each entry in params must have the same shape as yq
        assert params["mu"].shape == yq.shape
        assert params["sigma"].shape == torch.Size([params["sigma"].shape[0],params["sigma"].shape[1],params["sigma"].shape[1]])
        
        log_probs = torch.distributions.multivariate_normal.MultivariateNormal(params["mu"],params["sigma"]).log_prob(yq)

        return log_probs