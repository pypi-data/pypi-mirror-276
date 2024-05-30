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

from .domain_1 import domain as domain_cls
from .cell_zones_5 import cell_zones as cell_zones_cls
from .registers import registers as registers_cls
from .variable import variable as variable_cls
from .reference_frame_9 import reference_frame as reference_frame_cls
from .use_custom_field_function import use_custom_field_function as use_custom_field_function_cls
from .custom_field_function_name import custom_field_function_name as custom_field_function_name_cls
from .value_14 import value as value_cls

class calculate_patch(Command):
    fluent_name = ...
    argument_names = ...
    domain: domain_cls = ...
    cell_zones: cell_zones_cls = ...
    registers: registers_cls = ...
    variable: variable_cls = ...
    reference_frame: reference_frame_cls = ...
    use_custom_field_function: use_custom_field_function_cls = ...
    custom_field_function_name: custom_field_function_name_cls = ...
    value: value_cls = ...
