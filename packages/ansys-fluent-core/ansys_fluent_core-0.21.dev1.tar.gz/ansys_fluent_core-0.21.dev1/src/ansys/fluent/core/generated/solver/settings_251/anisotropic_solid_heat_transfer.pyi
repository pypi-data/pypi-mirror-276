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

from .relaxation import relaxation as relaxation_cls
from .flux import flux as flux_cls
from .gradient import gradient as gradient_cls

class anisotropic_solid_heat_transfer(Group):
    fluent_name = ...
    child_names = ...
    relaxation: relaxation_cls = ...
    flux: flux_cls = ...
    gradient: gradient_cls = ...
