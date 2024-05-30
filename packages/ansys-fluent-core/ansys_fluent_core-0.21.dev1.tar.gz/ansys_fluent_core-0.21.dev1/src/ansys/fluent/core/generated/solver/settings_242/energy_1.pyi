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

from .phasic_wall_heat_flux_form import phasic_wall_heat_flux_form as phasic_wall_heat_flux_form_cls

class energy(Group):
    fluent_name = ...
    child_names = ...
    phasic_wall_heat_flux_form: phasic_wall_heat_flux_form_cls = ...
