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

from .enabled_16 import enabled as enabled_cls
from .turbulent_intensity_2 import turbulent_intensity as turbulent_intensity_cls
from .turbulent_viscosity_ratio_2 import turbulent_viscosity_ratio as turbulent_viscosity_ratio_cls

class localized_turb_init(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    turbulent_intensity: turbulent_intensity_cls = ...
    turbulent_viscosity_ratio: turbulent_viscosity_ratio_cls = ...
