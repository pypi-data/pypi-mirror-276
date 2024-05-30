byma.nuby.Continuation
======================

.. py:module:: byma.nuby.Continuation


Classes
-------

.. autoapisummary::

   byma.nuby.Continuation.bs
   byma.nuby.Continuation.Bf


Functions
---------

.. autoapisummary::

   byma.nuby.Continuation.newton
   byma.nuby.Continuation.step
   byma.nuby.Continuation.cont


Module Contents
---------------

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





.. py:class:: Bf

   Defines default options for the Bifurcation package


.. py:function:: step(x, f, df, dfmu, dx, dmu, **kwargs)

   Perform one step of the continuation.

   :param x: array_like
       Current state.
   :param f: callable
       Function to evaluate the Jacobian matrix with respect to state variable x.
   :param df: callable
       Function to evaluate the Jacobian matrix with respect to state variable x.
   :param dfmu: callable
       Function to evaluate the Jacobian matrix derivative with respect to parameter mu.
   :param dx: array_like
       Current tangent with respect to state variable.
   :param dmu: float or array_like
       Incremental change in the parameter value.
   :param kwargs: dict
       Additional keyword arguments.

   :return: tuple
       A tuple containing the updated state x and the norm of the correction and the derivative of x w.r.t parameter

   :description:
   This function performs one step of the continuation, updating the state variable x and the tangent dx using the provided functions for evaluating the Jacobian matrix and its derivative with respect to the parameter.


.. py:function:: cont(x0, dx0, start, f, df, dfmu, dmu=None, target=None, **kwargs)

   Perform a continuation in parameter value from a starting value to a target value or until the maximum iteration is met, with constant step size.

   This function performs a continuation in parameter space from a starting value to a target value, or until the maximum iteration is met, adjusting the state variable x along the way. The continuation is carried out using the provided functions for evaluating the Jacobian matrix and its derivative with respect to the parameter.

   :param x0: array_like
       Initial state.
   :param dx0: array_like
       Initial tangent with respect to state variable.
   :param start: float
       Starting parameter value.
   :param f: callable
       Function to evaluate the Jacobian matrix with respect to state variable x.
   :param df: callable
       Function to evaluate the Jacobian matrix with respect to state variable x and parameter mu.
   :param dfmu: callable
       Function to evaluate the Jacobian matrix derivative with respect to parameter mu.
   :param dmu: float or array_like, optional
       Incremental change in the parameter value for each iteration. If None and target is None, raises ValueError.
   :param target: float or None, optional
       Target parameter value. If None, continuation is performed until maxit_con iterations.
   :param kwargs: dict
       Additional keyword arguments for customization.
           maxit_con : int, optional
               Maximum number of continuation steps. Default is 1000.
           method : str, optional
               Continuation method ('normal' or 'pseudo-arclength'). Default is 'normal'.
           mode : str, optional
               Return mode ('partial' or 'full'). Default is 'partial'.
           Other keyword arguments : Additional parameters specific to the step function used internally.

   :return: tuple or array_like
       Depending on the mode specified in kwargs, returns either a tuple or an array.
           - In 'partial' mode, returns a tuple containing the final state x and the final parameter value mu.
           - In 'full' mode, returns an array containing all the states x, an array of the norm of the correction at each step, and the final parameter value mu (if target is None).

   :raises:
       ValueError: If either 'dmu' or 'target' should be not 'None' but are not provided.
       ValueError: If the provided continuation method is invalid. Choose either 'normal' or 'pseudo-arclength'.

   Examples
   =============
       >>> # Define the functions df and dfmu
       >>> def df(x, mu0):
       >>>     # Compute the Jacobian matrix with respect to state variable x and parameter mu
       >>>     pass
       >>> def dfmu(x, mu0):
       >>>     # Compute the Jacobian matrix derivative with respect to parameter mu
       >>>     pass
       >>> 
       >>> # Define the initial state and tangent
       >>> x0 = np.array([1.0, 2.0])
       >>> dx0 = np.array([0.1, 0.1])
       >>> 
       >>> # Perform continuation from start value to target value
       >>> start = 0.0
       >>> target = 1.0
       >>> result = cont(x0, dx0, start, df, dfmu, target=target, maxit_con=1000, method='normal', mode='full')
       >>> print(result)


