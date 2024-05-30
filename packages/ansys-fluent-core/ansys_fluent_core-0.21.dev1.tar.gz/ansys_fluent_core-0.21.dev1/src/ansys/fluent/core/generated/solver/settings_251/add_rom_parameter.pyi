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

from .parameter_type import parameter_type as parameter_type_cls
from .entity_list import entity_list as entity_list_cls
from .group_value import group_value as group_value_cls
from .individual_or_group import individual_or_group as individual_or_group_cls
from .individual_value import individual_value as individual_value_cls
from .value_list import value_list as value_list_cls

class add_rom_parameter(Command):
    fluent_name = ...
    argument_names = ...
    parameter_type: parameter_type_cls = ...
    entity_list: entity_list_cls = ...
    group_value: group_value_cls = ...
    individual_or_group: individual_or_group_cls = ...
    individual_value: individual_value_cls = ...
    value_list: value_list_cls = ...
