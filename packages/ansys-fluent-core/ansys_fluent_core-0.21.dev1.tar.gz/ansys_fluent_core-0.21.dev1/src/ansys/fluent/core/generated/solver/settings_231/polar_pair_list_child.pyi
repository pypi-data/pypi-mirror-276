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

from .polar_real_angle import polar_real_angle as polar_real_angle_cls
from .polar_real_intensity import polar_real_intensity as polar_real_intensity_cls

class polar_pair_list_child(Group):
    fluent_name = ...
    child_names = ...
    polar_real_angle: polar_real_angle_cls = ...
    polar_real_intensity: polar_real_intensity_cls = ...
