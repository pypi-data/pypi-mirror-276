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

from .x_3 import x as x_cls
from .y_3 import y as y_cls
from .z_3 import z as z_cls

class u(Group):
    fluent_name = ...
    child_names = ...
    x: x_cls = ...
    y: y_cls = ...
    z: z_cls = ...
