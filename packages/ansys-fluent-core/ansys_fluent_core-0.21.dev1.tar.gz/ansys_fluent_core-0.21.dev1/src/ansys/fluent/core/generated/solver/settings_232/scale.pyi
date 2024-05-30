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

from .x_scale import x_scale as x_scale_cls
from .y_scale import y_scale as y_scale_cls
from .z_scale import z_scale as z_scale_cls

class scale(Command):
    fluent_name = ...
    argument_names = ...
    x_scale: x_scale_cls = ...
    y_scale: y_scale_cls = ...
    z_scale: z_scale_cls = ...
