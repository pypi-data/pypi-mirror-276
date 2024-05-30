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

from .enabled_9 import enabled as enabled_cls
from .turbulent_approximation import turbulent_approximation as turbulent_approximation_cls

class convective_heat_transfer(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    turbulent_approximation: turbulent_approximation_cls = ...
