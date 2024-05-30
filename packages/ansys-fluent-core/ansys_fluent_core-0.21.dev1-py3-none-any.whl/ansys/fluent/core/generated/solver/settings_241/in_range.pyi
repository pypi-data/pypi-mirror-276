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

from .value1 import value1 as value1_cls
from .value2 import value2 as value2_cls

class in_range(Group):
    fluent_name = ...
    child_names = ...
    value1: value1_cls = ...
    value2: value2_cls = ...
