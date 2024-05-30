import numpy as np
from ..interface.BaseInterface import BaseInterface as bs
from .Numy import Numy as Nu
from ..iteral import newton
import scipy.sparse as sp

    
class _root():
        
    def g(u, z, t, f, dt=0.01, i=1):
        return u - i*dt * f(x = u, t = t) - z
        
    def dg(u, z, t, df, dt=0.01, i=1):
        n = len(z)
        return sp.identity(n) - i*dt * df(x = u, t = t)
    
_DEFAULT_OPTS = {
    'stop': 'normal', 
    'maxit': 1e4, 
    'tol': 1e-8, 
    'verbose': False,
    'mode': None, 
    'method': 'backward',
    }

@bs.set_defaults(default_cls = Nu, default_opts=_DEFAULT_OPTS)
def euler(start=0, T=1, dt=0.01, x0=None, f=None, df=None, **kwargs):
    """
    Euler integration method.

    Parameters
    ----------
    start : float, optional
        Start time of integration (default: 0).
    T : float, optional
        End time of integration (default: 1).
    dt : float, optional
        Time step for integration (default: 0.01).
    x0 : numpy.ndarray, optional
        Initial condition (default: None).
    f : callable, optional
        Function representing the derivative of the system (default: None).
    df : callable, optional
        Function representing the derivative of the derivative of the system (default: None).
    **kwargs : dict, optional
        Additional keyword arguments.

    Returns
    -------
    sol : list
        List containing the solution at each time step.
    iter_list : list
        List containing the norm of the change in solution at each iteration.
    time : numpy.ndarray
        Array containing the time steps.

    Raises
    ------
    ValueError
        If x0, f, or df is None.
        If an invalid continuation method is provided.

    Notes
    -----
    This function implements the Euler integration method for solving ordinary differential equations.

    Examples
    --------
    >>> import numpy as np
    >>> from byma.numy import euler
    >>> def f(x, t):
    ...     return -x * t
    >>> sol, iter_list, time = euler(f=f, x0=1, T=1, dt=0.1)
    """
    _opts = bs.opts(**kwargs)
    verbose = _opts['verbose']
    method = _opts['method']
    
    # netwon default parameters for euler method
    kwargs['mode'] = 'partial'
    kwargs['stop'] = 'normal'

    # Set some parameters
    bs.check_none(x0, f, df)
    time = np.arange(start, T, dt)
    
    if verbose:
        print('------ Euler Method summary ------')
        print(f'Starting time: {start}')
        print(f'Ending time: {T}')
        print(f'Time step: {dt}')
        print(f'method: {method}')
    
        print('------ Start iteration ------')
        
        
    # Time loop 
    sol = []
    iter_list = []
    func = _root
    for i,t in enumerate(time):

        f1 = lambda x: func.g(u=x, z=x, t=t, f=f, dt=dt, i=i)
        df1 = lambda x: func.dg(u=x, z=x, t=t, df=df, dt=dt, i=i)
        
        if method == 'backward':
            x0, dxnorm = newton(x = x0, f = f1, df = df1, **kwargs)
        elif method == 'foward':
            raise ValueError("Foward Euler method is not yet avialible")
        elif method == 'trapezoidal':
            raise ValueError("Trapezoidal method is not yet avialible")
        else:
            raise ValueError("Invalid continuation method. Choose either 'backward', 'foward' or 'trapezoidal'.")

        if (verbose != 0 and verbose != False) and (i % verbose == 0):
            print(f'Solution at time {t} is {x0}')
            
        sol.append(x0.copy())
        
        iter_list.append(dxnorm)
        
    return sol, iter_list, time