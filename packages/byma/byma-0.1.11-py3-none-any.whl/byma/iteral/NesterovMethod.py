import numpy as np
from ..interface.BaseInterface import BaseInterface as bs
from .Iteral import Iteral as Int
from numpy import linalg as npling
from scipy.optimize import line_search
import warnings
import scipy.sparse as sp

_DEFAULT_OPTS = {
    'stop': 'normal', 
    'maxit': 1e4, 
    'tol': 1e-8, 
    'verbose': False,
    'mode': None, 
    'method': 'normal',
    'delta_x': 0.0005,
    "dim": 1,
    "domain": None, 
    "l": 1,
    "alpha": None,
    "gamma": 1,
    }


def _returns(minx, fnorm, dxnorm, mode, method):
    """
    Helper function to format the return value based on the mode.

    Parameters
    ----------
    x : array_like
        Root obtained after iterations.
    fnorm : float
        Norm of the residuals.
    dxnorm : float
        Norm of the correction.
    mode : str
        Mode of the output ('full', 'partial', None).
    method : str
        Stopping method used.

    Returns
    -------
    tuple
        Tuple containing the formatted output based on the mode.
    """
    
    if mode == 'full':
        return minx, dxnorm, fnorm
    elif mode == 'partial':
        if method == 'normal': 
            return minx[-1], dxnorm 
        else: 
            return minx[-1], fnorm
        
    elif ((mode == None) or (mode == False)):
        return minx[-1], dxnorm, fnorm


def calc_numerical_gradient(f, x, delta_x):
    """Function for computing gradient numerically."""
    val_at_x = f(x)
    val_at_next = f(x + delta_x)
    return (val_at_next - val_at_x) / delta_x
                

@bs.set_defaults(default_cls = Int, default_opts=_DEFAULT_OPTS)
def nesterov(x, f, df, **kwargs):
    """
    Perform Nesterov's acceleration method iterations to find the minimizer of a given function.

    Parameters
    ----------
    x : array_like
        Initial guess.
    f : callable
        Function to minimize.
    df : callable/Null
        Jacobian matrix.
    **kwargs : dict
        Additional keyword arguments for customization.
        
        domain : collable. 
            Domain. If collable, input x return Boolean. True if inside domain. Default R^n
        dim :   int. 
            Diamension starting space. Default R. 
        tol : float, optional
            Tolerance for convergence. Default is 1e-8.
        maxit : int, optional
            Maximum number of iterations. Default is 10000.
        verbose : bool, optional
            If True, prints iteration information. Default is False.
        mode : str, optional
            Mode of the output ('full', 'partial', None).
            
        stop :  int. Default 0. Default optimal 
                    0: ||grad(f)||<tol
        L : float
            smooth constant
    
    Returns
    -------
    minimize, correction_norm, residuals_norm : tuple
        If mode is 'full'
    minimize, correction_norm, (residuals_norm) : tuple
        if mode is 'partial'. The residuals_norm are returned if method is not 'normal' 
    
    minimize, iterations, correction_norm, residuals_norm: tuple
        if mode is None

    Raises
    ------
    ValueError
        If the maximum number of iterations or tolerance is not a positive integer.

    Examples
    --------
    Basic usage:
    """   

    # Initialize the known constants
    _opts = bs.opts(**kwargs)
    verbose = _opts['verbose']
    mode = _opts['mode']
    tol = _opts['tol']
    maxit = int(_opts['maxit'])
    stop = _opts['stop']
    delta_x = _opts['delta_x']
    dim = _opts['dim']
    domain = _opts['domain'] 
    L = _opts['l']
    gamma = _opts['gamma']
    lambda_prev = 0
    lambda_curr = 1
    y_prev = x
    alpha = _opts['alpha'] if _opts['alpha'] != None else 0.05 / (2 * L)
    
    
    ##### Checking correctness parameters #####
    
    assert isinstance(dim, int), "dim must be an integer"
    
    if maxit <= 0 or not isinstance(maxit, int):
        raise ValueError("Maximum number of iterations 'maxit' must be a positive integer.")
    if tol <= 0:
        raise ValueError("Tolerance 'tol' must be a positive value.")
    
    if df == None:
        assert delta_x > 0, "Step must be positive."
        df = lambda x: calc_numerical_gradient(f, x, delta_x)
        
    if verbose:
        print('------ Nesterov Method summary ------')
        print(f'tollerence: {tol}')
        print(f'maximum iter: {maxit}')
        print(f'stopping criteria: {stop}')
        print(f'starting guess: {x}')
        print(f'alpha: {alpha}')
        print(f'L: {L}')
        print(f'gamma: {gamma}')
    
        print('------ Start iteration ------')
        
    # initialize solution lists
    f_value = f(x)
    df_value = df(x)
    normdx = []
    normf = []
    minx = []
    
    for iter in range(maxit):
        
        # Initialize the prescibe type of method 
        y_curr = x - alpha * df(x)
        x = (1 - gamma) * y_curr + gamma * y_prev
        y_prev = y_curr

        lambda_tmp = lambda_curr
        lambda_curr = (1 + np.sqrt(1 + 4 * lambda_prev * lambda_prev)) / 2
        lambda_prev = lambda_tmp

        gamma = (1 - lambda_prev) / lambda_curr
    
        
        if sp.issparse(f_value) and sp.issparse(df_value):
            fnorm = sp.linalg.norm(f(x))
            dxnorm = sp.linalg.norm(df(x))
        else:
            fnorm = np.linalg.norm(f(x))
            dxnorm = np.linalg.norm(df(x))
            
        normdx.append(dxnorm)
        normf.append(fnorm)
        minx.append(x)
        
        if  (verbose != 0 and verbose != False) and (iter % verbose == 0):
            print(f"Nesterov method  status at iteration {iter + 1}: ||dx|| = {dxnorm} and ||F|| = {fnorm}")
        
        if (fnorm < tol and stop == 'residual-check'):
            if verbose:
                print(f'Nesterov method converged in {iter + 1} iterations with ||F|| = {fnorm}')
            return _returns(minx, fnorm=normf, dxnorm=normdx, mode=mode, method=stop)
        
        if (dxnorm < tol and stop == 'normal'):
            if verbose:
                print(f'Nesterov method  converged in {iter + 1} iterations with ||dx|| = {dxnorm}')
            return _returns(minx, fnorm=normf, dxnorm=normdx, mode=mode, method=stop)
       
        if domain != None:
            if domain(x) == False:
                print('Guess is out of bounds')
                break
        
    if verbose:
        print(f'Nesterov method did not converge within {maxit} iterations')

    return _returns(minx, fnorm=normf, dxnorm=normdx, mode=mode, method=stop)