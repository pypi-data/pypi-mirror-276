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
    "step": 0,
    "beta": 1,
    "domain": None, 
    "L": 1,
    "gamma": 1,
    "sigma": 0.5,
    "alpha": None,
    "c": 1,
    "p": 1
    }


def _returns(minx, fnorm, dxnorm, mode, method):
    """
    Helper function to format the return value based on the mode.

    Parameters
    ----------
    minx : array_like
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

## Armijo stepsize
def step_size_armijo(beta, sigma, gamma, x, d, f, df):
    """
    Armijo's Rule
    """
    i = 0
    inequality_satisfied = True
    while inequality_satisfied:
        if df(x + np.power(beta, i)*gamma * d(x)) <= f(x) + gamma * np.power(beta, i) * sigma * df(x).dot(
                d(x)):
            break

        i += 1

    return np.power(beta, i)

def _step(step, f, df, sigma, alpha, gamma, x, c, p, iter, beta):
    """
    Check type of step
    """
    
    if step == 1:
        k = iter
        alpha = c*(k**(-p))
        
    elif step == 2:
        alpha = gamma*step_size_armijo(beta, sigma, gamma=gamma, x=x, d=d, f=f, df=df)
        
    elif step == 3:
        
        if iter != 0:
            g = df(x)
            beta = (npling.norm(g)/npling.norm(dxnorm))**2
            d = -g + beta*dk
                
        # Perform the line search to find the step size
        with warnings.catch_warnings(record=True) as w:
            dk = d(x) if iter == 0 else d
            result = line_search(f=f, myfprime=df, xk=x, pk=dk)

        # Check for LineSearchWarning
        if any(isinstance(warn.message, warnings.WarningMessage) and 'The line search algorithm did not converge' in str(warn.message) for warn in w):
            raise ValueError('Line search did not converge.')      

        # Extract the step size from the result
        alpha = result[0]
        if alpha == None:
            raise ValueError('Alpha is a NoneType => line search did not converge')

        dxnorm = df(x)
        
    return alpha
            
        

@bs.set_defaults(default_cls = Int, default_opts=_DEFAULT_OPTS)
def gradient_descent(x, f, df, **kwargs):
    """
    Perform Gradient Descent iterations to find the minimizer of a given function.

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
        step :  int. Default 1/L
                    0: constant method
                    1: vanishing method
                    2: armijo method
                    3: Fletcher-reeves method 
            
        stop :  int. Default 0. Default optimal 
                    0: ||grad(f)||<tol
        beta : float
            armijo parameter. Defaul 1
        gamma : float
            2nd armijo parameter. Default 1/L
        alpha : float
            step size. Default 1/L
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
    step = _opts['step']
    delta_x = _opts['delta_x']
    dim = _opts['dim']
    domain = _opts['domain'] 
    L = _opts['L']
    c = _opts['c']
    p = _opts['p']
    alpha = _opts['alpha'] if _opts['alpha'] != None else 1/L
    sigma = _opts['sigma']
    gamma = _opts['gamma']
    beta = _opts['beta']  
    gamma = gamma if gamma != 0 else alpha
    
    
    iterative = lambda x, alpha, d: x + alpha * d(x) if callable(d) else x + alpha * d
    d = lambda x: - df(x)

    ##### Checking correctness parameters #####
    
    assert isinstance(dim, int), "dim must be an integer"
    
    if maxit <= 0 or not isinstance(maxit, int):
        raise ValueError("Maximum number of iterations 'maxit' must be a positive integer.")
    if tol <= 0:
        raise ValueError("Tolerance 'tol' must be a positive value.")
    
    if df == None:
        assert delta_x > 0, "Step must be positive."
        df = lambda x: calc_numerical_gradient(f, x, delta_x)
        
    if  step != 1 and step != 2 and step != 3 and step != 0:
        raise ValueError('the type must be either of the following:  0/floar: constant method 1: vanishing method 2: armijo method 3: Fletcher-reeves method')

    if verbose:
        print('------ Gradient Descent Method summary ------')
        print(f'tollerence: {tol}')
        print(f'maximum iter: {maxit}')
        print(f'stopping criteria: {stop}')
        print(f'starting guess: {x}')
        print(f'step size type: {step}')
        print(f'alpha: {alpha}')
        print(f'L: {L}')
        if step == 1:
            print(f'p: {p}')
            print(f'c: {c}')
        if step == 2:
            print(f'gamma: {gamma}')
            print(f'beta: {beta}')
    
        print('------ Start iteration ------')
        
    # initialize solution lists
    f_value = f(x)
    df_value = df(x)
    normdx = []
    normf = []
    minx = []
    
    
    for iter in range(maxit):
        
        # Initialize the prescibe type of method 
        alpha = _step(step, f, df, sigma, alpha, gamma, x, c, p, iter, beta)
        
        # Iteration Step
        x = iterative(x, alpha, d)
        
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
            print(f"Gradient Descent  status at iteration {iter + 1}: ||dx|| = {dxnorm} and ||F|| = {fnorm}")
        
        if (fnorm < tol and stop == 'residual-check'):
            if verbose:
                print(f'Gradient Descent converged in {iter + 1} iterations with ||F|| = {fnorm}')
            return _returns(minx, fnorm=normf, dxnorm=normdx, mode=mode, method=stop)
        
        if (dxnorm < tol and stop == 'normal'):
            if verbose:
                print(f'Gradient Descent  converged in {iter + 1} iterations with ||dx|| = {dxnorm}')
            return _returns(minx, fnorm=normf, dxnorm=normdx, mode=mode, method=stop)
       
        if domain != None:
            if domain(x) == False:
                print('Guess is out of bounds')
                break
        
    if verbose:
        print(f'Gradient Descent did not converge within {maxit} iterations')

    return _returns(minx, fnorm=normf, dxnorm=normdx, mode=mode, method=stop)