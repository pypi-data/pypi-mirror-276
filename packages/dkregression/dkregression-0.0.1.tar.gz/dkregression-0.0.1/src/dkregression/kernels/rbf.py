import torch

class RBF():
    """
    The radial basis function (RBF) kernel or squared exponential kernel, how it sometimes is also referred to uses a bell curve to calculate the relationship between two points $x_1, x_2\in\mathbb{R}^d$ in space. It has one (hyper)parameter: the sacale length $\ell$. Let $\mathbf{x}_1\in\mathbb{R}^{m\\times d}$ be a matrix that represents $m$ $d$-dimensional points and $\mathbf{x}_2\in\mathbb{R}^{n\\times d}$ be a matrix that represents $n$ $d$-dimensional points, then the RBF kernel is defined as:
    $$
    k(\mathbf{x}_1,\mathbf{x}_2)=\exp\left(-\\frac{\lVert\mathbf{x}_2 - \mathbf{x}_1\\rVert_L^2}{2\ell^2}\\right)~.
    $$
    $L$ is the distance norm used. The kernel matrix is of shape $k(\mathbf{x}_1,\mathbf{x}_2)\in\mathbb{R}^{n\\times m}$.
        
    Attributes:
        param_names (list): A list of strings that contains the names of the model parameters. For the RBF kernel, this is the scale length 'l'.
        dist_norm (float): The L distance norm to be used to calculate the pairwise distances in the RBF kernel function. Value needs to fulfill `0<dist_norm`.
        k_nearest_initial_guess (int): The $k$ used in the heuristic to calculate teh average distance between all points in the dataset and their k-nearest point which is used as initial guess for the kernel scale length $\ell$.
        params (dict): Contains the current estimate of the kernel hyperparameter $\ell$. The keys are defined in `RBF.param_names`. For the RBF kernel the only key of this dictionary is 'l'. Upon creating the RBF object, an initial guess for the scale length is calculated as the average distance of the `k_nearest_initial_guess`-th closest point for each point in `X`. This ensures that on average, a sufficient number of points contribute to the kernel regression, at least for the inital guess.
        params_lower_bound (dict): Same keys as defined in `RBF.params_names`, provide the lower bounds for the kernel parameters ($\ell$ for the RBF). The value is determined by multiplying the factor `RBF.lower_bound_multiplier` with the inital guess for each of kernel parameters.
        params_upper_bound (dict): Same keys as defined in `RBF.params_names`, provide the upper bounds for the kernel parameters ($\ell$ for the RBF). The value is determined by multiplying the factor `RBF.upper_bound_multiplier` with the inital guess for each of kernel parameters.

    Examples:
        ```py
        import torch
        from dkregression.kernels import RBF
        from dkregression.likelihoods import UnivariateGaussianLikelihood
        from dkregression.cross_validation import CrossValidation
        from dkregression import DKR

        X = torch.rand((100,2))
        Y = torch.rand((100,1))

        kernel = RBF(X,dist_norm=1) # using the L1-norm
        likelihood = UnivariateGaussianLikelihood()
        cv = CrossValidation()

        model = DKR(kernel, likelihood, cv)
        model.fit(X,Y)
        ```
    
    """
    def __init__(self,x,dist_norm=2,lower_bound_multiplier=0.2,upper_bound_multiplier=5,k_nearest_initial_guess=10) -> None:
        """Initialization of the RBF object.

        Args:
            x (torch.Tensor): Set of data points used to initizalize the kernel. Needs to be two-dimensional of shape `(n,d)` with `n` being the number of points and `d` being the dimenionsionality. This determines the initial guess for the kernel parameter $\ell$ as well as the upper and lower bounds of $\ell$ if the `DKR.fit` method is used.
            dist_norm (float, optional): Order of the norm that is used for calculating the pairwise distance between two points. 
            lower_bound_multiplier (float, optional): Factor by which the inital guess for the kernel parameters should be multiplied to obtain a lower bound for the search conducted in `DKR.fit`. Value should fulfill `0<=lower_bound_multiplier<=1`.
            upper_bound_multiplier (int, optional): Factor by which the inital guess for the kernel parameters should be multiplied to obtain a upper bound for the search conducted in `DKR.fit`. Value should fulfill `1<=upper_bound_multiplier`.
            k_nearest_initial_guess (int, optional): The $k$ used in the heuristic to calculate the average distance between all points in the dataset and their k-nearest point which is used as initial guess for the kernel scale length $\ell$.
        """
        # expects x.shape = (n,d)
        self.param_names = ["l"]
        self.dist_norm = dist_norm
        self.k_nearest_initial_guess = k_nearest_initial_guess
        self.lower_bound_multiplier = lower_bound_multiplier
        self.upper_bound_multiplier = upper_bound_multiplier
        self.init_params(x)
        
        
    def init_params(self,x) -> None:
        original_x_dim = x.shape[0]
        x = torch.unique(x,dim=0) # in case multiple data points are the same
        if original_x_dim != x.shape[0]:
            print("There are multiple data points in your dataset with the same x-value.")
        d = torch.linalg.norm(x.unsqueeze(1)-x.unsqueeze(0),dim=-1,ord=self.dist_norm)
        k_closest = min(x.shape[0],self.k_nearest_initial_guess)
        avg_dist = -torch.topk(-d,k_closest,dim=0).values[-1,:].mean() #average distance to the 10th closest point
        self.params = {"l":avg_dist.item()} #set initial value for scale length l
        self.params_lower_bound = {p:self.lower_bound_multiplier*self.params[p] for p in self.params}
        self.params_upper_bound = {p:self.upper_bound_multiplier*self.params[p] for p in self.params}
        # self.precomputed_self_kernel_matrix = self.kernel_matrix(x,x)   # precompute the kernel matrix

    
    def kernel_matrix(self,x1,x2,normalize_dim=1) -> torch.Tensor:
        """Returns the kernel matrix for the RBF kernel based on two sets of input points `x1`, and `x2`.

        Args:
            x1 (torch.Tensor): First set of input points. Needs to have shape `(n,d)`. Even for the one-dimensional case, the shape needs to be `(n,1)`.
            x2 (torch.Tensor): First set of input points. Needs to have shape `(m,d)`. Even for the one-dimensional case, the shape needs to be `(m,1)`.
            normalize_dim (int, optional): Specifies if and in which dimension the kernel matrix should be normalized. `normalize_dim=-1` indicated no normalization, `normalize_dim=0` indicates column-wise normalization, and `normalize_dim=1` indicates row-wise normalization.

        Returns:
            (torch.Tensor): The kernel matrix of shape `(m,n)`. If `normalize` is set to `True`, the kernel matrix is normalized row-wise, i.e., `kernel_matrix(x1,x2,normalize=True)[i,:].sum()==1`. 

        Examples:
        ```py
        import torch
        from dkregression.kernels import RBF

        X1 = torch.rand((100,2))
        X2 = torch.rand((50,2))

        # the initialization is mandatory to set an initial value for the scale length
        kernel = RBF(X1) 
        k = kernel.kernel_matrix(X1,X2)
        print(k.shape)
        ```
        This results in the following output:
        ```
        torch.Size([50, 100])
        ```
        """

        #expect that x.shape = (n,d)
        # distance matrix
        d = torch.linalg.norm(x1.unsqueeze(0)-x2.unsqueeze(1),dim=-1,ord=self.dist_norm)

        # calculate the log kernel matrix
        log_k = -d**2/(2*self.params["l"]**2)

        if normalize_dim in [0,1]:
            k = torch.softmax(log_k,dim=normalize_dim)  #this should be numerically more stable than normalizing exp(k)
        elif normalize_dim == -1:
            k = torch.exp(log_k)
        else:
            raise NotImplementedError("The normalization dimension needs to be non-negative integer identifying the dimension along which the kernel matrix should be normalized or -1 to indicate that no normalization should occur.")

        return k