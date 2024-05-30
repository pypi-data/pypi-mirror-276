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

from .symbol import symbol as symbol_cls
from .size import size as size_cls
from .color_1 import color as color_cls

class markers_child(Group):
    fluent_name = ...
    child_names = ...
    symbol: symbol_cls = ...
    size: size_cls = ...
    color: color_cls = ...
