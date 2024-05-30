byma.interface
==============

.. py:module:: byma.interface

.. autoapi-nested-parse::

   BaseInterface Module
   ====================

   This module provides a base interface for defining default classes and options. It includes functionality for setting default parameters, updating interface options, and retrieving updated options.



Submodules
----------

.. toctree::
   :maxdepth: 1

   /autoapi/byma/interface/BaseInterface/index
   /autoapi/byma/interface/NonlinearHeat/index
   /autoapi/byma/interface/Time/index


Classes
-------

.. autoapisummary::

   byma.interface.BaseInterface
   byma.interface.NonlinearHeat
   byma.interface.TimeRecorder
   byma.interface.TimeRecorder


Functions
---------

.. autoapisummary::

   byma.interface.annotate
   byma.interface.time
   byma.interface.set_quiet
   byma.interface.read_data


Package Contents
----------------

.. py:class:: BaseInterface(default_cls, default_opts, **kwargs)

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





.. py:class:: NonlinearHeat

   Damped stationary heat equation with discretization using finite difference method.

   The equation is given by:

   .. math::
       u_{xx} + \mu(u - \frac{1}{3}u^3)   x \in [0,1]
       u(0) = 1, u(1) = 0

   The linearized version is:

   .. math::
       u_{xx} + \mu u    x \in [0,1]
       u(0) = 1, u(1) = 0

   Functions:

   - `GL1(x, mu)`: Checks if x is a zero of the right-hand side.
   - `fGL1(u, n, mu)`: Computes the resulting sparse matrix.
   - `linGL1(n)`: Computes a 1d float vector for the linearized version.
   - `JacGL1(u, n, mu)`: Computes the Jacobian matrix.



   .. py:method:: GL1(x, mu)

      Computes the finite difference method for the damped stationary heat equation.

      Parameters
      ----------
      x : numpy.ndarray
          1D vector.
      mu : float
          Scalar parameter.

      Returns
      -------
      numpy.ndarray
          Result of the computation.




   .. py:method:: fGL1(**kwargs)

      Computes the resulting sparse matrix for the damped stationary heat equation.

      Parameters
      ----------
      **kwargs : dict
          Keyword arguments including 'u', 'n', and 'mu'.

      Returns
      -------
      numpy.ndarray
          Resulting sparse matrix.




   .. py:method:: linGL1(n, **kwargs)

      Computes a 1D float vector for the linearized version of the heat equation.

      Parameters
      ----------
      n : int
          Number of grid points.

      Returns
      -------
      numpy.ndarray
          1D float vector.




   .. py:method:: JacGL1(**kwargs)

      Computes the Jacobian matrix for the damped stationary heat equation.

      Parameters
      ----------
      **kwargs : dict
          Keyword arguments including 'u', 'n', and 'mu'.

      Returns
      -------
      numpy.ndarray
          Jacobian matrix.




.. py:class:: TimeRecorder(quiet_mode: bool = False)

   .. py:method:: reset()

      Clear all recorded time statistics.



   .. py:method:: start(block_name: str)

      Record the start time of a code block.

      Parameters:
      -----------
      block_name : str
          Name of the code block.
          
      Examples:
      ---------
      >>> recorder.start("my_block")



   .. py:method:: end(block_name: str, quiet: Optional[bool] = None) -> float

      Record the end time of a code block and calculate the elapsed time.

      Parameters:
      -----------
      block_name : str
          Name of the code block.
      quiet : bool, optional
          Whether to suppress printing the time measurement. Default is None.

      Returns:
      --------
      float
          Elapsed time in milliseconds.
          
      Examples:
      ---------
      >>> elapsed_time = recorder.end("my_block")



   .. py:method:: report(percent_of: str = None, reset: bool = False)

      Generate and print a report of recorded time statistics.

      Parameters:
      -----------
      percent_of : str, optional
          Name of the code block for which to generate the report as a percentage. Default is None.
      reset : bool, optional
          Whether to reset the recorded time statistics after generating the report. Default is False.
          
      Examples:
      ---------
      >>> recorder.report()



.. py:function:: annotate(func: Callable, quiet: Optional[bool])

   Annotate a function or code block to measure its execution time.

   Parameters:
   -----------
   func : callable
       Function or code block to annotate.
   quiet : bool, optional
       Whether to suppress printing the time measurement. Default is None.
       
   Examples:
   ---------
   >>> @annotate(quiet=True)
   ... def my_function():
   ...     pass


.. py:function:: time(func_or_name: Union[Callable, str] = None, quiet: Optional[bool] = None, save_to_h5: Optional[bool] = None, filename: Optional[str] = None, rewrite: Optional[bool] = None, plot_title: Optional[str] = None, h5_graph_title: Optional[str] = None, **kwargs)

   Measure the execution time of a function or code block.

   Parameters:
   -----------
   func_or_name : callable or str, optional
       Function or code block to measure execution time. Default is None.
   quiet : bool, optional
       Whether to suppress printing the time measurement. Default is None.
   save_to_h5 : bool, optional
       Whether to save the time measurements to an HDF5 file. Default is None.
   h5_filename : str, optional
       Name of the HDF5 file to save time measurements. Default is None.
   h5_rewrite : bool, optional
       Whether to overwrite the existing HDF5 file. Default is None.
   h5_plot_title : str, optional
       Title of the plot generated from the HDF5 file. Default is None.
   h5_graph_title : str, optional
       Title of the graph generated from the HDF5 file. Default is None.
   kwargs : dict, optional
       Additional keyword arguments for customization.

   Returns:
   --------
   function or _timeblock
       Annotated function or context manager.
       
   Examples:
   ---------
   >>> @time
   ... def my_function():
   ...     pass


.. py:function:: set_quiet(quiet: bool = True)

   Set the quiet mode for suppressing time measurements.

   Parameters:
   -----------
   quiet : bool, optional
       Whether to suppress printing the time measurement. Default is True.
       
   Examples:
   ---------
   >>> set_quiet(True)


.. py:function:: read_data(filename: str, data_names: list)

   Read data from an HDF5 file.

   Parameters:
   -----------
   filename : str
       Name of the HDF5 file.
   data_names : list
       List of data names to read from the HDF5 file.

   Returns:
   --------
   dict
       Dictionary containing the data read from the HDF5 file.
       
   Examples:
   ---------
   >>> data = read_data('timings.h5', ['Block1'])


.. py:class:: TimeRecorder(quiet_mode: bool = False)

   .. py:method:: reset()

      Clear all recorded time statistics.



   .. py:method:: start(block_name: str)

      Record the start time of a code block.

      Parameters:
      -----------
      block_name : str
          Name of the code block.
          
      Examples:
      ---------
      >>> recorder.start("my_block")



   .. py:method:: end(block_name: str, quiet: Optional[bool] = None) -> float

      Record the end time of a code block and calculate the elapsed time.

      Parameters:
      -----------
      block_name : str
          Name of the code block.
      quiet : bool, optional
          Whether to suppress printing the time measurement. Default is None.

      Returns:
      --------
      float
          Elapsed time in milliseconds.
          
      Examples:
      ---------
      >>> elapsed_time = recorder.end("my_block")



   .. py:method:: report(percent_of: str = None, reset: bool = False)

      Generate and print a report of recorded time statistics.

      Parameters:
      -----------
      percent_of : str, optional
          Name of the code block for which to generate the report as a percentage. Default is None.
      reset : bool, optional
          Whether to reset the recorded time statistics after generating the report. Default is False.
          
      Examples:
      ---------
      >>> recorder.report()



