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

from .domain import domain as domain_cls
from .cell_zones import cell_zones as cell_zones_cls
from .register_id import register_id as register_id_cls
from .variable import variable as variable_cls
from .patch_velocity import patch_velocity as patch_velocity_cls
from .use_custom_field_function import use_custom_field_function as use_custom_field_function_cls
from .custom_field_function_name import custom_field_function_name as custom_field_function_name_cls
from .value_1 import value as value_cls

class calculate_patch(Command):
    fluent_name = ...
    argument_names = ...
    domain: domain_cls = ...
    cell_zones: cell_zones_cls = ...
    register_id: register_id_cls = ...
    variable: variable_cls = ...
    patch_velocity: patch_velocity_cls = ...
    use_custom_field_function: use_custom_field_function_cls = ...
    custom_field_function_name: custom_field_function_name_cls = ...
    value: value_cls = ...
