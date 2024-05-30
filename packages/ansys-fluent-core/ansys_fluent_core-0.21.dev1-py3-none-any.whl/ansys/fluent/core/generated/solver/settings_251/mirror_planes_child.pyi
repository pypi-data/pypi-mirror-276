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

from .plane_coefficients import plane_coefficients as plane_coefficients_cls
from .distance import distance as distance_cls
from .visible_1 import visible as visible_cls

class mirror_planes_child(Group):
    fluent_name = ...
    child_names = ...
    plane_coefficients: plane_coefficients_cls = ...
    distance: distance_cls = ...
    visible: visible_cls = ...
