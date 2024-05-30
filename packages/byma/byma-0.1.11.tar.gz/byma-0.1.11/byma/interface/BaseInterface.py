import functools

class BaseInterface:
    '''Defines a base interface'''

    def __init__(self, default_cls, default_opts, **kwargs):
        self.cls = default_cls
        self.default_opts = default_opts
        self.kwargs = kwargs

    @staticmethod
    def set_defaults(default_cls, default_opts={}):
        """
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
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(**kwargs):
                
                _opts = default_cls()._opts.copy()
                _opts.update(default_opts)
                
                kwargs['default_opts'] = _opts
                kwargs['default_cls'] = default_cls

                return func(**kwargs)
            return wrapper
        return decorator

    @staticmethod
    def opts(**kwargs):
        """
        Method for setting options for the interface.

        Parameters
        ----------
        kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        dict
            A dictionary containing updated interface and parameters.
        """
        # Construct instance of default class with the updated interface and parameters 
        usr_opts = kwargs.pop('usr_opts', None) 
        _opts = kwargs.pop('default_opts') 
        

        if usr_opts is not None:
            _opts.update(usr_opts)
            
        _opts.update(kwargs)

        return dict(_opts)
    
    def check_none(*args):
        """
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

        
        """
        none_indices = [i for i, arg in enumerate(args) if arg is None]
        if none_indices:
            none_names = [args[i].__name__ if hasattr(args[i], '__name__') else str(args[i]) for i in none_indices]
            raise ValueError(f"The following arguments are None: {', '.join(none_names)}")
