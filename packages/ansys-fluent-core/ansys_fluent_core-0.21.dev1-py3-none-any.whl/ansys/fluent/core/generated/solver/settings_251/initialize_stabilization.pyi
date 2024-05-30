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

from .strategy_1 import strategy as strategy_cls
from .scheme_1 import scheme as scheme_cls

class initialize_stabilization(Group):
    fluent_name = ...
    command_names = ...

    def strategy(self, ):
        """
        Initialize the blended stabilization strategies: reset to the 1st scheme.
        """

    def scheme(self, ):
        """
        Initialize the stabilization scheme.
        """

