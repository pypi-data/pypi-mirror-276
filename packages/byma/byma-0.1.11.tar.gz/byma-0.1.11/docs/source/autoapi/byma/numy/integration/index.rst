byma.numy.integration
=====================

.. py:module:: byma.numy.integration


Classes
-------

.. autoapisummary::

   byma.numy.integration.bs
   byma.numy.integration.Nu


Functions
---------

.. autoapisummary::

   byma.numy.integration.newton
   byma.numy.integration.euler


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





.. py:class:: Nu

   Defines default options for the numerical methods sub-package


.. py:function:: newton(x, f, df, **kwargs)

   Perform Newton iterations to find the root of a given function.

   Parameters
   ----------
   x : array_like
       Initial guess for the root.
   f : callable
       Function to evaluate the residuals.
   df : callable
       Function to evaluate the Jacobian matrix.
   **kwargs : dict
       Additional keyword arguments for customization.
       tol : float, optional
           Tolerance for convergence. Default is 1e-8.
       maxit : int, optional
           Maximum number of iterations. Default is 10000.
       verbose : bool, optional
           If True, prints iteration information. Default is False.
       mode : str, optional
           Mode of the output ('full', 'partial', None).

   Returns
   -------
   root, correction_norm, residuals_norm : tuple
       If mode is 'full'
   root, correction_norm, (residuals_norm) : tuple
       if mode is 'partial'. The residuals_norm are returned if method is not 'normal' 

   root, iterations, correction_norm, residuals_norm: tuple
       if mode is None

   Raises
   ------
   ValueError
       If the maximum number of iterations or tolerance is not a positive integer.

   Examples
   --------
   Basic usage:
   >>> root, iterations, norm_correction = newton(2.0, lambda x: x**2 - 4, lambda x: 2 * x, verbose=True)
   >>> print("Root:", root, "Iterations:", iterations, "Norm of correction:", norm_correction)
       
   Usage with kwargs provided as a dictionary:
   >>> kwargs = {'verbose': True, 'tol': 1e-6, 'maxit': 20}
   >>> root, norm_correction = newton(3.0, lambda x: x**3 - 27, lambda x: 3 * x**2, **kwargs)
   >>> print("Root:", root, "Norm of correction:", norm_correction)


.. py:function:: euler(start=0, T=1, dt=0.01, x0=None, f=None, df=None, **kwargs)

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


