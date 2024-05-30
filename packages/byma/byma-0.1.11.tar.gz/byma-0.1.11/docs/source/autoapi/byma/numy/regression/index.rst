byma.numy.regression
====================

.. py:module:: byma.numy.regression


Classes
-------

.. autoapisummary::

   byma.numy.regression.bs
   byma.numy.regression.nu


Functions
---------

.. autoapisummary::

   byma.numy.regression.gradient_descent
   byma.numy.regression.nesterov
   byma.numy.regression.objective
   byma.numy.regression.read
   byma.numy.regression.regression


Module Contents
---------------

.. py:class:: bs(default_cls, default_opts, **kwargs)

   Defines a base interface


   .. py:method:: set_defaults(default_cls, default_opts={})
      :staticmethod:


      Decorator for setting default interface and parameters.

      Parameters
      ----------
      default_cls : obj
          The default class instance.
      default_opts : dict, optional
          Default options for the interface (default is an empty dictionary).

      Returns
      -------
      callable
          A decorator function that sets default interface and parameters.



   .. py:method:: opts(**kwargs)
      :staticmethod:


      Method for setting options for the interface.

      Parameters
      ----------
      kwargs : dict
          Additional keyword arguments.

      Returns
      -------
      dict
          A dictionary containing updated interface and parameters.



   .. py:method:: check_none()

      Check if any of the arguments are None.

      Parameters
      ----------
      *args : tuple
          Arbitrary number of arguments to check.

      Returns
      -------
      bool
          True if any argument is None, False otherwise.

      Raises
      ------
      ValueError
          If any argument is None, raises ValueError with the names of the None arguments.





.. py:class:: nu

   Defines default options for the numerical methods sub-package


.. py:function:: gradient_descent(x, f, df, **kwargs)

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


.. py:function:: nesterov(x, f, df, **kwargs)

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


.. py:function:: objective(basis, degree, u)

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


.. py:function:: read(dataset, ext, input, output)

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


.. py:function:: regression(dataset=None, input=None, output=None, **kwargs)

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


