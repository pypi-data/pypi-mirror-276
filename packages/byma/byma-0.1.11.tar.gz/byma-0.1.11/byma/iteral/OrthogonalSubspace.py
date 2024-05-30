import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import splu
from numpy.linalg import qr
from ..interface.BaseInterface import BaseInterface as bs
from .Iteral import Iteral as Int
import scipy.sparse as sp

_DEFAULT_OPTS = {
        'stop': 'matrix',
        'maxit': 1e4,
        'tol': 1e-8,
        'which': 'SM',
        'verbose': True,
    }


    
def _Z(X, A = None, which = 'SM'):
    if sp.issparse(A) == False:
        A = csc_matrix(A)
    if which == 'SM':
        z = splu(A).solve(X)
    else:
        z = A @ X
    return z

@bs.set_defaults(default_cls = Int, default_opts=_DEFAULT_OPTS)
def osim(A, V = None, k = None, **kwargs):
    """
    Orthogonal Subspace Iteration Method (OSIM).

    Args:
    A : numpy.ndarray
        The matrix to compute the eigenvalues and eigenvectors for.
    V : numpy.ndarray
        Initial guess of eigenvectors. Default None,
    k : int
        number of desired eigenvalues. Default None. 
    

    Keyword Arguments:
        tol : float, optional
            Tolerance for convergence (default: 1e-8).
        maxit : int, optional
            Maximum number of iterations (default: 100).
        stop : str, optional
            Stopping criteria for convergence. Options are 'eig' (default), 'matrix', or 'residual'.
        which : str, optional
            If small or biggest eigenvalues. Default "SM" = smallest. 
        verbose : bool, optional
            If True, prints iteration information (default: True).

    Returns:
    numpy.ndarray
        Matrix of eigenvectors.
    numpy.ndarray
        Matrix of transformed eigenvectors.
    tuple
        Tuple containing eigenvalues at each iteration.

    Notes:
    This function implements the Orthogonal Subspace Iteration Method (OSIM) to compute eigenvectors and eigenvalues of a matrix A.

    Examples:
    >>> import numpy as np
    >>> from byma.interal import osim
    >>> A = np.array([[1, 0], [0, 1]])
    >>> V = np.array([[1], [0]])
    >>> V, BV, iter = osim(A, V, tol=1e-8, maxit=1000, stop='eig')

    You can also pass keyword arguments using a dictionary. For example:
    >>> kwargs = {'tol': 1e-8, 'maxit': 1000, 'stop': 'eig'}
    >>> V, BV, iter = osim(A, V, **kwargs)

    You can also pass keyword arguments using two separate dictionaries for parameters and interface. For example:
    >>> parameters = {'tol': 1e-8, 'maxit': 1000, 'stop': 'eig'}
    >>> interface = {'verbose': True}
    >>> V, BV, iter = sosim(A, V, parameters=parameters, interface=interface)
    """
    
    _opts = bs.opts(**kwargs)
    verbose = _opts['verbose']
    tol = _opts['tol']
    maxit = int(_opts['maxit'])
    stop = _opts['stop']
    which = _opts['which']
    
    # Check if the number of rows of V matches the number of columns of A
    if V != None:
        if V.shape[0] != A.shape[1]:
            raise ValueError("Number of rows of V must match the number of columns of A.")
    else:
        if k == None:
            raise ValueError("Either V or k should be not-None")
        else:
            V = np.random.rand(A.shape[1], k)
    
    if verbose:
        print('------ OSIM initialization summary ------')
        print(f'tollerence: {tol}')
        print(f'maximum iter: {maxit}')
        print(f'stopping criteria: {stop}')
        print(f'Required eig: {which}')
    
        print('------ Start iteration ------')

    B = lambda V: V.T @ _Z(X = V, A = A, which= which)

    iter = []
    for n in range(maxit):
        Zn = _Z(X = V, A = A, which= which)
        BV = B(V = V)
        eig = np.diag(BV)
        if which == 'SM':
            eig = 1/eig
        if verbose != False: 
            if (n % verbose == 0):
                print(f"Eigenvalues at n = {n}: {eig}")
        else:
            if (n % 5000 == 0):
                print(f"iteration n = {n}")
        
        if n > 0:
            iter.append(eig)
        
        V, _ = qr(Zn)

        if stop == 'eig':
            if n > 1:
                if abs(np.linalg.norm(eig - iter[n - 1])) < tol:
                    print(f'The Orthogonal Subspace Method has converged in {n} iterations.')
                    break
            else:
                pass
        elif stop == 'matrix':
            
            if n > 1:
                if np.linalg.norm(BV - B(V)) < tol:
                    print(f'The Orthogonal Subspace Method has converged in {n} iterations.')
                    break
        
        elif stop == 'residual':
            
            if np.linalg.norm(A @ V - V @ B(V)) < tol:
                print(f'The Orthogonal Subspace Method has converged in {n} iterations.')
                break
    
        if n >= maxit:
            print('The Orthogonal Subspace Method has not converged')
        
    return V, BV, tuple(iter)
        
        

    
    