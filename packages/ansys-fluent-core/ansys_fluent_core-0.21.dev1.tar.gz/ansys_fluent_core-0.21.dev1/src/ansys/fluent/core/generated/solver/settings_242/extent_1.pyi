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

from .theta_3 import theta as theta_cls
from .radial_2 import radial as radial_cls
from .axial_1 import axial as axial_cls

class extent(Group):
    fluent_name = ...
    child_names = ...
    theta: theta_cls = ...
    radial: radial_cls = ...
    axial: axial_cls = ...
