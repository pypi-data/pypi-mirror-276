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

from .selection_3 import selection as selection_cls
from .options_20 import options as options_cls
from .limits_1 import limits as limits_cls
from .default_limits import default_limits as default_limits_cls
from .initialize_3 import initialize as initialize_cls

class design_variables(Group):
    fluent_name = ...
    child_names = ...
    selection: selection_cls = ...
    options: options_cls = ...
    limits: limits_cls = ...
    command_names = ...

    def default_limits(self, ):
        """
        Reset design variables limits to default.
        """

    def initialize(self, ):
        """
        Initialize the design variables with the current values.
        """

