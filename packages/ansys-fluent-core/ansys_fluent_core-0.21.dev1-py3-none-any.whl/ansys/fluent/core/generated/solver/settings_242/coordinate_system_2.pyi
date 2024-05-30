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

from .origin_3 import origin as origin_cls
from .axis_4 import axis as axis_cls
from .radial_1 import radial as radial_cls

class coordinate_system(Group):
    fluent_name = ...
    child_names = ...
    origin: origin_cls = ...
    axis: axis_cls = ...
    radial: radial_cls = ...
