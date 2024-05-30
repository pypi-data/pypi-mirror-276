byma.interface.Time
===================

.. py:module:: byma.interface.Time

.. autoapi-nested-parse::

   Time Module
   ===========

   This module provides functionality for measuring and recording the execution time of functions or code blocks. It offers methods to annotate functions for time measurement, record time statistics, save data to HDF5 files, and more.

   Examples
   ============
       >>> from byma.interface import TimeRecorder, time, set_quiet, read_data

       >>> # Create a TimeRecorder object with quiet mode enabled
       >>> recorder = TimeRecorder(quiet_mode=True)

       >>> # Annotate a function to measure its execution time
       >>> @time
       ... def my_function():
       ...     time.sleep(1)
       ...
       >>> my_function()
       >>> # Output depends on the quiet mode setting

       >>> # Measure execution time using a context manager
       >>> with time("Block1"):
       ...     time.sleep(0.5)
       ...
       Block1 took 500.12ms

       >>> # Generate and print a report of recorded time statistics
       >>> recorder.report()
       time report...
                        Block1:  500.12ms for      1 calls
                    my_function: 1000.23ms for      1 calls

       >>> # Reset recorded time statistics
       >>> recorder.reset()

       >>> # Set quiet mode to suppress printing time measurements
       >>> set_quiet(True)
       >>> my_function()
       >>> # No output since quiet mode is enabled

       >>> # Save time measurements to an HDF5 file
       >>> with time(save_to_h5=True):
       ...     time.sleep(0.3)
       ...
       >>> # Data saved to 'timings.h5' file

       >>> # Read data from an HDF5 file
       >>> data = read_data('timings.h5', ['Block1'])
       >>> print(data)
       {'Block1': array(500.12)}
       
   Acknowledgement
   ===================

   This module has been made by taking inspiration and multiple parts of the code from the `timebudget` package.



Classes
-------

.. autoapisummary::

   byma.interface.Time.TimeRecorder


Functions
---------

.. autoapisummary::

   byma.interface.Time.annotate
   byma.interface.Time.time
   byma.interface.Time.set_quiet
   byma.interface.Time.read_data


Module Contents
---------------

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


