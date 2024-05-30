byma.numy
=========

.. py:module:: byma.numy

.. autoapi-nested-parse::

   ``byma.numy``
   ================

   The ByMa basic numerical methods sub-package.

   Functions present in byma.numy are listed below.


   Continuation
   --------------------------

      euler
      

   Exceptions
   ----------

      NuMyError



Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/byma/numy/Numy/index
   /autoapi/byma/numy/integration/index
   /autoapi/byma/numy/regression/index


Classes
-------

.. autoapisummary::

   byma.numy.Numy


Functions
---------

.. autoapisummary::

   byma.numy.euler
   byma.numy.regression


Package Contents
----------------

.. py:class:: Numy

   Defines default options for the numerical methods sub-package


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


