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

from .planar_conductivity import planar_conductivity as planar_conductivity_cls
from .transverse_conductivity import transverse_conductivity as transverse_conductivity_cls

class biaxial(Group):
    fluent_name = ...
    child_names = ...
    planar_conductivity: planar_conductivity_cls = ...
    transverse_conductivity: transverse_conductivity_cls = ...
