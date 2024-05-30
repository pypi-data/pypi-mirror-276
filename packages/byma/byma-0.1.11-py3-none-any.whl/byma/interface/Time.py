"""
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

"""

import sys
from time import time as pytime
import warnings
from collections import defaultdict
from functools import wraps
from typing import Callable, Optional, Union
import h5py

class TimeRecorder:
    def __init__(self, quiet_mode: bool = False):
        """
        Initialize a TimeRecorder object.

        Parameters:
        -----------
        quiet_mode : bool, optional
            Whether to suppress printing time measurements. Default is False.
            
        Examples:
        ---------
        >>> recorder = TimeRecorder(quiet_mode=True)
        """

        self.quiet_mode = quiet_mode
        self.reset()
        self.out_stream = sys.stdout

    def reset(self):
        """Clear all recorded time statistics."""
        self.start_times = {}
        self.elapsed_total = defaultdict(float)
        self.elapsed_cnt = defaultdict(int)

    def _print(self, msg: str):
        """Print a message."""
        self.out_stream.write(msg + "\n")
        self.out_stream.flush()

    def start(self, block_name: str):
        """
        Record the start time of a code block.

        Parameters:
        -----------
        block_name : str
            Name of the code block.
            
        Examples:
        ---------
        >>> recorder.start("my_block")
        """

        if block_name in self.start_times:
            warnings.warn(f"time is confused: time.start({block_name}) without end")
        self.start_times[block_name] = pytime()

    def end(self, block_name: str, quiet: Optional[bool] = None) -> float:
        """
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
        """

        if quiet is None:
            quiet = self.quiet_mode
        if block_name not in self.start_times:
            warnings.warn(f"time is confused: time.end({block_name}) without start")
            return float('NaN')
        elapsed = 1000 * (pytime() - self.start_times[block_name])
        self.elapsed_total[block_name] += elapsed
        self.elapsed_cnt[block_name] += 1
        del self.start_times[block_name]
        if not quiet:
            self._print(f"{block_name} took {self._format_time(elapsed)}")
        return elapsed

    def _format_time(self, milliseconds: float) -> str:
        """
        Format elapsed time.

        Parameters:
        -----------
        milliseconds : float
            Elapsed time in milliseconds.

        Returns:
        --------
        str
            Formatted elapsed time.
            
        Examples:
        ---------
        >>> formatted_time = recorder._format_time(1000.234)
        """

        return f"{milliseconds:.3f}ms" if milliseconds < 1 else f"{milliseconds:.2f}ms" if milliseconds < 1000 else f"{milliseconds/1000:.3f}sec"

    def report(self, percent_of: str = None, reset: bool = False):
        """
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
        """

        results = []
        for name, cnt in self.elapsed_cnt.items():
            total = self.elapsed_total[name]
            results.append({
                'name': name,
                'total': total,
                'cnt': cnt,
                'avg': total / cnt,
            })
        results = sorted(results, key=lambda r: r['total'], reverse=True)
        if percent_of:
            assert percent_of in self.elapsed_cnt, f"Can't generate report for unrecognized block {percent_of}"
            self._print(f"time report per {percent_of} cycle...")
            total_elapsed = self.elapsed_total[percent_of]
            total_cnt = self.elapsed_cnt[percent_of]
            for res in results:
                avg = res['total'] / total_cnt
                pct = 100.0 * res['total'] / total_elapsed
                avg_cnt = res['cnt'] / total_cnt
                self._print(f"{res['name']:>25s}:{pct: 6.2f}% {avg: 8.2f}ms/cyc @{avg_cnt: 8.1f} calls/cyc")
        else:
            self._print("time report...")
            for res in results:
                self._print(f"{res['name']:>25s}:{res['total']: 8.2f}ms for {res['cnt']: 6d} calls")
        if reset:
            self.reset()

_default_recorder = TimeRecorder()

def annotate(func: Callable, quiet: Optional[bool]):
    """
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
    """

    name = func.__name__
    @wraps(func)
    def inner(*args, **kwargs):
        _default_recorder.start(name)
        try:
            return func(*args, **kwargs)
        finally:
            _default_recorder.end(name, quiet)
    return inner

class _timeblock():
    def __init__(self, name: str, quiet: Optional[bool]):
        self.name = name
        self.quiet = quiet

    def __enter__(self):
        _default_recorder.start(self.name)

    def __exit__(self, typ, val, trace):
        _default_recorder.end(self.name, self.quiet)

def time(func_or_name: Union[Callable, str] = None, quiet: Optional[bool] = None, save_to_h5: Optional[bool] = None, filename: Optional[str] = None, rewrite: Optional[bool] = None, plot_title: Optional[str] = None, h5_graph_title: Optional[str] = None, **kwargs):
    """
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
    """

    save_to_h5 = kwargs.get('save_to_h5', False) if save_to_h5 is None else save_to_h5
    filename = kwargs.get('filename', 'timings.h5') if filename is None else filename
    rewrite = kwargs.get('rewrite', True) if rewrite is None else rewrite
    plot_title = kwargs.get('plot_title', 'Timing Data') if plot_title is None else plot_title
    h5_graph_title = kwargs.get('h5_graph_title', 'Functions') if h5_graph_title is None else h5_graph_title

    if isinstance(func_or_name, str):  # If block name is provided
        return _timeblock(func_or_name, quiet)
    else:  # If a function is provided
        def wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs):
                result = None
                block_name = func.__name__
                _default_recorder.start(block_name)
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    elapsed_time = _default_recorder.end(block_name, quiet)
                    if save_to_h5 and filename:
                        with h5py.File(filename, 'a') as f:
                            if rewrite:
                                if block_name in f:
                                    del f[block_name]
                            f.create_dataset(block_name, data=elapsed_time)

            return inner

        return wrapper(func_or_name)

def set_quiet(quiet: bool = True):
    """
    Set the quiet mode for suppressing time measurements.

    Parameters:
    -----------
    quiet : bool, optional
        Whether to suppress printing the time measurement. Default is True.
        
    Examples:
    ---------
    >>> set_quiet(True)
    """

    _default_recorder.quiet_mode = quiet

def read_data(filename: str, data_names: list):
    """
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
    """

    data = {}
    with h5py.File(filename, 'r') as f:
        for name in data_names:
            if name in f:
                data[name] = f[name][()]
    return data
