#
# This is an auto-generated file.  DO NOT EDIT!
#


from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from typing import Union, List, Tuple

from .enable_1 import enable as enable_cls
from .disable import disable as disable_cls
from .print import print as print_cls
from .clear import clear as clear_cls

class profile(Group):
    fluent_name = ...
    command_names = ...

    def enable(self, ):
        """
        Enable adaption profiling.
        """

    def disable(self, ):
        """
        Disable adaption profiling.
        """

    def print(self, ):
        """
        Print adaption profiling results.
        """

    def clear(self, ):
        """
        Clear adaption profiling counters.
        """

