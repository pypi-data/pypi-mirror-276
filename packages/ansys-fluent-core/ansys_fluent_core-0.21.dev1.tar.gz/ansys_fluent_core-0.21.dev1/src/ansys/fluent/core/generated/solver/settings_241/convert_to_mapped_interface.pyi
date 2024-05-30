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

from .all import all as all_cls
from .auto import auto as auto_cls
from .use_local_edge_length_factor import use_local_edge_length_factor as use_local_edge_length_factor_cls
from .gtol_length_factor import gtol_length_factor as gtol_length_factor_cls
from .gtol_absolute_value import gtol_absolute_value as gtol_absolute_value_cls

class convert_to_mapped_interface(Command):
    fluent_name = ...
    argument_names = ...
    all: all_cls = ...
    auto: auto_cls = ...
    use_local_edge_length_factor: use_local_edge_length_factor_cls = ...
    gtol_length_factor: gtol_length_factor_cls = ...
    gtol_absolute_value: gtol_absolute_value_cls = ...
