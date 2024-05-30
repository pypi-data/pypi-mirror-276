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

from .value_18 import value as value_cls
from .affected_conditions import affected_conditions as affected_conditions_cls

class parameters_child(Group):
    fluent_name = ...
    child_names = ...
    value: value_cls = ...
    affected_conditions: affected_conditions_cls = ...
