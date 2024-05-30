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

from .file_name_22 import file_name as file_name_cls
from .observable_2 import observable as observable_cls
from .value_17 import value as value_cls
from .weight_4 import weight as weight_cls
from .expected_change import expected_change as expected_change_cls

class results_child(Group):
    fluent_name = ...
    child_names = ...
    file_name: file_name_cls = ...
    observable: observable_cls = ...
    value: value_cls = ...
    weight: weight_cls = ...
    expected_change: expected_change_cls = ...
