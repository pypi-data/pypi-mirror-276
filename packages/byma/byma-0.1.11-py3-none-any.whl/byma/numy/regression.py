import numpy as np
from ..interface.BaseInterface import BaseInterface as bs
from .Numy import Numy as nu
from ..iteral import gradient_descent, nesterov
import pandas as pd 
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import lsqr

_DEFAULT_OPTS = {
    'verbose': False,
    'mode': None, 
    'method': 'nesterov',
    'dloss': None,
    'loss': 'mse',
    'degree': 3,
    'extension': None
    }
       
def objective(basis, degree, u):
    """
    Computes the design matrix A for a given basis function, degree, and input data u.
    The design matrix A is constructed by stacking the basis functions column-wise, 
    and then concatenating a column of ones to the left.
    
    Parameters
    ----------
    basis : callable
        A callable basis function
    degree : int
        The degree of the basis function
    u : array-like
        The input data
    
    Returns
    -------
    A : csc_matrix
        The design matrix as a compressed sparse column (CSC) matrix
    """
    A = np.column_stack([[basis(u[i], j) for i in range(len(u))] for j in range(1, degree + 1)])
    # Create the matrix H by concatenating ones column-wise
    A = np.column_stack([np.ones(len(u)), A])
    return csc_matrix(A)   

def read(dataset, ext, input, output):
    """
    Reads data from a pandas dataset and extracts the input and output variables.
    
    Parameters
    ----------
    dataset : str or pandas.DataFrame
        The pandas dataset to read from
    ext : str
        The file extension of the dataset (either 'csv' or 'xlsx')
    input : str
        The column name of the input variable
    output : str
        The column name of the output variable
    
    Returns
    -------
    data : pandas.DataFrame
        The original pandas dataset
    u : array-like
        The input data as a numpy array
    v : array-like
        The output data as a numpy array
    """
    if ext == 'cvs':
        data = pd.read_csv(dataset)
    elif ext == 'xlsx':
        data = pd.read_excel(dataset)
    else:
        data = dataset
    
    assert dataset != None, 'Dataset cannot be None'
    
    v = np.array([data[output]]).T
    u = np.array(data[input])
    
    return data, u, v
    
    
        

@bs.set_defaults(default_cls = nu, default_opts=_DEFAULT_OPTS)
def regression(dataset=None, input=None, output=None, **kwargs):
    """
    Performs a regression analysis on a given dataset using a specified basis function and loss function.
    
    Parameters
    ----------
    dataset : str or pandas.DataFrame, optional
        The pandas dataset to analyze (default is None)
    input : str, optional
        The column name of the input variable (default is None)
    output : str, optional
        The column name of the output variable (default is None)
    **kwargs : dict
        Additional keyword arguments for the regression algorithm    
        
    Returns
    -------
    x : array-like
        The coefficients of the regression model
    
    Raises
    ------
    ValueError
        If the dataset is None
    
    Examples
    --------
    Basic usage:
    >>> regression(dataset='data.csv', input='x', output='y')
    """
    
    _opts = bs.opts(**kwargs)
    verbose = _opts['verbose']
    method = _opts['method']
    ext = _opts['extension']
    verbose = _opts['verbose']
    loss = _opts['loss']
    basis = _opts['basis']
    degree = _opts['degree']
    dloss = _opts['dloss']
    
    if verbose:
        print('------ Regression initialization summary ------')
        print(f'Dataset used: {dataset}')
        print(f'Dataset input: {input}')
        print(f'Dataset ouput: {output}')
    
        print('------ Start iteration ------')

    _, u, v = read(dataset, ext, input, output)
    

    if loss == "mse" and basis == None:
        basis = lambda u, i: u**i
        A = objective(basis, degree, u)
        # Solve the normal equation H^T H x = H^T b
        x, _, _, _ = lsqr(A.T @ A,  A.T @ v)[:4] 
        return x 
    elif loss == "mse" and basis != None:
        A = objective(basis, degree, u)
        # Solve the normal equation H^T H x = H^T b
        x, _, _, _ = lsqr(A.T @ A,  A.T @ v)[:4] 
        return  x
    else:
        f = lambda x: loss(x, u, v, **kwargs)
        df = lambda x: dloss(x, u, v, **kwargs)
        kwargs['f'] = f
        kwargs['df'] = df
        
    
    if method == "nesterov":
        return nesterov(**kwargs)
    else:
        return gradient_descent(**kwargs)