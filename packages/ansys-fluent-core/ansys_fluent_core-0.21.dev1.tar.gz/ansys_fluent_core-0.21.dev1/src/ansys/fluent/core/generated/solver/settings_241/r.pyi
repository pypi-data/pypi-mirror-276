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

from .x import x as x_cls
from .y import y as y_cls
from .z import z as z_cls

class r(Group):
    fluent_name = ...
    child_names = ...
    x: x_cls = ...
    y: y_cls = ...
    z: z_cls = ...
