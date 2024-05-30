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

from .count_1 import count as count_cls
from .parameters_count import parameters_count as parameters_count_cls
from .parameters_5 import parameters as parameters_cls
from .conditions_2 import conditions as conditions_cls

class operating_conditions(Group):
    fluent_name = ...
    child_names = ...
    count: count_cls = ...
    parameters_count: parameters_count_cls = ...
    parameters: parameters_cls = ...
    conditions: conditions_cls = ...
