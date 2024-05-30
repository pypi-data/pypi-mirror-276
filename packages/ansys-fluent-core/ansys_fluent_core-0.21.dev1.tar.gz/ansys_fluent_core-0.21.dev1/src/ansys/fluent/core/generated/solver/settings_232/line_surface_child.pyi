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

from .name_2 import name as name_cls
from .p0 import p0 as p0_cls
from .p1 import p1 as p1_cls

class line_surface_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    p0: p0_cls = ...
    p1: p1_cls = ...
