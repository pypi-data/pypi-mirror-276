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

from .isat_error_tolerance import isat_error_tolerance as isat_error_tolerance_cls
from .isat_table_size import isat_table_size as isat_table_size_cls
from .isat_verbosity import isat_verbosity as isat_verbosity_cls
from .clear_isat_table import clear_isat_table as clear_isat_table_cls

class isat_options(Group):
    fluent_name = ...
    child_names = ...
    isat_error_tolerance: isat_error_tolerance_cls = ...
    isat_table_size: isat_table_size_cls = ...
    isat_verbosity: isat_verbosity_cls = ...
    command_names = ...

    def clear_isat_table(self, ):
        """
        Clear the current ISAT table.
        """

