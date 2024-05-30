:orphan:

:py:mod:`byma.nuby._nuby`
=========================

.. py:module:: byma.nuby._nuby

.. autoapi-nested-parse::

   Notes
   -----
   This module is has basic bifurcation analysis tools



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   byma.nuby._nuby.Bifurcation



Functions
~~~~~~~~~

.. autoapisummary::

   byma.nuby._nuby.step
   byma.nuby._nuby.cont



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


.. py:class:: Bifurcation


   Defines default options for the Bifurcation package


