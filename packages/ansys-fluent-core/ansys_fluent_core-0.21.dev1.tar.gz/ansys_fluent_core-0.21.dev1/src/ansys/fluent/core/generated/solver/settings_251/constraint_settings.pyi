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

from .second_order import second_order as second_order_cls
from .increase_local_smoothness import increase_local_smoothness as increase_local_smoothness_cls
from .increase_global_smoothness import increase_global_smoothness as increase_global_smoothness_cls
from .tolerance_4 import tolerance as tolerance_cls

class constraint_settings(Group):
    fluent_name = ...
    child_names = ...
    second_order: second_order_cls = ...
    increase_local_smoothness: increase_local_smoothness_cls = ...
    increase_global_smoothness: increase_global_smoothness_cls = ...
    tolerance: tolerance_cls = ...
