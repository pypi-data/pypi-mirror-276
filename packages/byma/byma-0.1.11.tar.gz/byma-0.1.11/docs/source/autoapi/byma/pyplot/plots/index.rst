byma.pyplot.plots
=================

.. py:module:: byma.pyplot.plots


Functions
---------

.. autoapisummary::

   byma.pyplot.plots.plot_scale
   byma.pyplot.plots.plot
   byma.pyplot.plots.plot_numerical_error


Module Contents
---------------

.. py:function:: plot_scale(x, y, label, scale, style={})

   Plot data with specified scale and style.

   Parameters
   ================
   x : array-like
       Data points for the x-axis.
   y : array-like
       Data points for the y-axis.
   label : str
       Label for the data.
   scale : str
       Scale for the plot. Options: 'normal', 'loglog', 'xlog', 'ylog'.
   style : dict or None, optional
       Dictionary specifying line style. If None, default style is used.

   Returns
   -------
   None

   Examples
   ================
   Plotting with different scales:

   >>> import numpy as np
   >>> import matplotlib.pyplot as plt
   >>> import byma.pyplot as byplt

   >>> x = np.linspace(0.1, 10, 100)
   >>> y = np.sin(x)

   # Normal scale
   >>> plt.figure()
   >>> byplt.plot_scale(x, y, label='sin(x)', scale='normal')
   >>> plt.legend()
   >>> plt.show()

   # Log-log scale
   >>> plt.figure()
   >>> byplt.plot_scale(x, y, label='sin(x)', scale='loglog')
   >>> plt.legend()
   >>> plt.show()

   # Semi-log x scale
   >>> plt.figure()
   >>> byplt.plot_scale(x, y, label='sin(x)', scale='xlog')
   >>> plt.legend()
   >>> plt.show()

   # Semi-log y scale
   >>> plt.figure()
   >>> byplt.plot_scale(x, y, label='sin(x)', scale='ylog')
   >>> plt.legend()
   >>> plt.show()


.. py:function:: plot(x=None, y=None, **kwargs)

   Function that creates plots of different kinds. With this function, it is possible to plot n numbers of 
   function in the same figure quickly and with high personalization.

   Parameters
   ==============
   x : array-like
       Array of x values.
   y : array-like
       Array of y values.
   **kwargs : dict, optional
       settings (dict): Overall plot settings.
           title (str): Title of the plot.
           xlabel (str): Label for the x-axis.
           ylabel (str): Label for the y-axis.
           label (str):  Label for the 1st function.
           label{i} (str): Label for the ith function from i=1.
           x{i} (array-like): Array of x values for the ith function from i=1.
           y{i} (array-like): Array of y values for the ith function from i=1.
           save_title (str): File name to save the plot.
           save_path (str): Path to save the plot. If None, the plot will be saved in the current directory.
           scale (str): Scale for the plot. Options: 'normal', 'loglog', 'xlog', 'ylog'.
           style{i} (dic, string): Dictionary, string having customization from the matplotlib functions, like style

   Returns
   ===========
   A plot


.. py:function:: plot_numerical_error(n, func, solve_func, save_title=None, save_path=None, **kwargs)

   Plot the numerical error between the exact and numerical solutions and print the maximum error.

   Parameters
   ----------
   n : int
       Number of grid points.
   func : object
       Instance of the class containing the exact solution.
   solve_func : function
       Function to solve the system.
   save_title : str, optional
       File name plot.
   save_path : str, optional
       Path to save the plot. If None, the plot will be saved in the current directory.
   **kwargs : dict, optional
       Additional keyword arguments to customize the plot and title for saving.

   Returns
   -------
   None


