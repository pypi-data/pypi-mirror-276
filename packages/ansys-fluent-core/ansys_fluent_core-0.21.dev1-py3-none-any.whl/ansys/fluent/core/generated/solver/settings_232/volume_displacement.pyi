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

from .option import option as option_cls
from .ddpm_phase import ddpm_phase as ddpm_phase_cls

class volume_displacement(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    ddpm_phase: ddpm_phase_cls = ...
