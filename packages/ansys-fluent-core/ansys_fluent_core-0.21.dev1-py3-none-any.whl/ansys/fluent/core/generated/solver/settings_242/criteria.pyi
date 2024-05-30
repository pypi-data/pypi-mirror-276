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

from .min_cell_volume import min_cell_volume as min_cell_volume_cls
from .min_orthogonal import min_orthogonal as min_orthogonal_cls
from .print_current_status import print_current_status as print_current_status_cls

class criteria(Group):
    fluent_name = ...
    child_names = ...
    min_cell_volume: min_cell_volume_cls = ...
    min_orthogonal: min_orthogonal_cls = ...
    command_names = ...

    def print_current_status(self, ):
        """
        Print current mesh quality metrics.
        """

