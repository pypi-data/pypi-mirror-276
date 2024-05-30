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

from .name_2 import name as name_cls
from .retain_instantaneous_values import retain_instantaneous_values as retain_instantaneous_values_cls
from .input_params import input_params as input_params_cls
from .function_name import function_name as function_name_cls
from .average_over import average_over as average_over_cls
from .old_props import old_props as old_props_cls

class user_defined_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    retain_instantaneous_values: retain_instantaneous_values_cls = ...
    input_params: input_params_cls = ...
    function_name: function_name_cls = ...
    average_over: average_over_cls = ...
    old_props: old_props_cls = ...
