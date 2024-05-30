:orphan:

:py:mod:`byma.numy._numy`
=========================

.. py:module:: byma.numy._numy

.. autoapi-nested-parse::

   Notes
   -----

   This module is has basic numerical methods tools



Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   byma.numy._numy.Numy



Functions
~~~~~~~~~

.. autoapisummary::

   byma.numy._numy.euler



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


.. py:class:: Numy


   Defines default options for the numerical methods sub-package


