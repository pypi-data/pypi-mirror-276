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

from .origin_2 import origin as origin_cls
from .x_axis_1 import x_axis as x_axis_cls
from .y_axis_1 import y_axis as y_axis_cls
from .z_axis_1 import z_axis as z_axis_cls

class current_state(Group):
    fluent_name = ...
    child_names = ...
    origin: origin_cls = ...
    x_axis: x_axis_cls = ...
    y_axis: y_axis_cls = ...
    z_axis: z_axis_cls = ...
