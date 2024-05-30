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

from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .gtol_length_factor import gtol_length_factor as gtol_length_factor_cls
from .gtol_absolute_value import gtol_absolute_value as gtol_absolute_value_cls
from .update import update as update_cls

class tolerance(Command):
    fluent_name = ...
    argument_names = ...
    use_local_edge_length_factor: use_local_edge_length_factor_cls = ...
    gtol_length_factor: gtol_length_factor_cls = ...
    gtol_absolute_value: gtol_absolute_value_cls = ...
    update: update_cls = ...
