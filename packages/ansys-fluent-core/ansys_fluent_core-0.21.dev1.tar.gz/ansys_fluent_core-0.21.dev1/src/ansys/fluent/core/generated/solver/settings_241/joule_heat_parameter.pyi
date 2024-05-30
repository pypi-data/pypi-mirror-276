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

from .enabled_12 import enabled as enabled_cls
from .value_2 import value as value_cls

class joule_heat_parameter(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    value: value_cls = ...
