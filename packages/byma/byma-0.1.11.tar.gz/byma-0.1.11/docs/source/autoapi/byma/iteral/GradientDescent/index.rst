byma.iteral.GradientDescent
===========================

.. py:module:: byma.iteral.GradientDescent


Classes
-------

.. autoapisummary::

   byma.iteral.GradientDescent.bs
   byma.iteral.GradientDescent.Int


Functions
---------

.. autoapisummary::

   byma.iteral.GradientDescent.calc_numerical_gradient
   byma.iteral.GradientDescent.step_size_armijo
   byma.iteral.GradientDescent.gradient_descent


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





.. py:class:: Int

   Defines default options for the Iterative methods sub-package


.. py:function:: calc_numerical_gradient(f, x, delta_x)

   Function for computing gradient numerically.


.. py:function:: step_size_armijo(beta, sigma, gamma, x, d, f, df)

   Armijo's Rule


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


