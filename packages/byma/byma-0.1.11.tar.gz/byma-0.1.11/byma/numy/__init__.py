"""
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

"""
# To get sub-modules
from . import _numy
from ._numy import *

__all__ = _numy.__all__.copy()