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

from .x_axis_5 import x_axis as x_axis_cls
from .y_axis_5 import y_axis as y_axis_cls

class labels(Group):
    fluent_name = ...
    child_names = ...
    x_axis: x_axis_cls = ...
    y_axis: y_axis_cls = ...
