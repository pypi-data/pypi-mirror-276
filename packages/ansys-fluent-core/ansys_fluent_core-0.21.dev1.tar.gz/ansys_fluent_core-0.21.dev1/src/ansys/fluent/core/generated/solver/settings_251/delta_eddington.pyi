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

from .forward_scattering_factor import forward_scattering_factor as forward_scattering_factor_cls
from .asymmetry_factor import asymmetry_factor as asymmetry_factor_cls

class delta_eddington(Group):
    fluent_name = ...
    child_names = ...
    forward_scattering_factor: forward_scattering_factor_cls = ...
    asymmetry_factor: asymmetry_factor_cls = ...
