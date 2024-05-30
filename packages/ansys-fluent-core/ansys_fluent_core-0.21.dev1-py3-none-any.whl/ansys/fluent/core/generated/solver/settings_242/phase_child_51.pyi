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

from .turbulence_4 import turbulence as turbulence_cls
from .geometry_3 import geometry as geometry_cls

class phase_child(Group):
    fluent_name = ...
    child_names = ...
    turbulence: turbulence_cls = ...
    geometry: geometry_cls = ...
