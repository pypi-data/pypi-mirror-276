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

from .x_5 import x as x_cls
from .y_5 import y as y_cls
from .background_color import background_color as background_color_cls

class axes(Group):
    fluent_name = ...
    child_names = ...
    x: x_cls = ...
    y: y_cls = ...
    background_color: background_color_cls = ...
