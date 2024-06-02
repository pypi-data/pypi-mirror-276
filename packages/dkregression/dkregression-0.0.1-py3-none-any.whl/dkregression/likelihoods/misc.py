import torch

def log_likelihood(x,y,xq,yq,kernel,likelihood,reduction='mean'):
    # allowed reductions are 'mean', 'sum', 'none'
    k = kernel.kernel_matrix(x,xq)
    params = likelihood.compute_params(k,x,y,kernel)
    log_likelihood = likelihood.evaluate_log_likelihood(yq,params)

    if reduction == 'sum':
        log_likelihood = log_likelihood.sum()
    elif reduction == 'mean':
        log_likelihood = log_likelihood.mean()
    elif reduction == 'none':
        pass
    else:
        raise NotImplementedError("Allowed reductions are 'mean', 'sum', and 'none'")
    
    return log_likelihood