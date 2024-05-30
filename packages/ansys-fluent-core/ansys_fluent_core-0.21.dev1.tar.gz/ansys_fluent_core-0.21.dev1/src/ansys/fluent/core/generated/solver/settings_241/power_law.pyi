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
from .b import b as b_cls
from .reference_viscosity import reference_viscosity as reference_viscosity_cls
from .reference_temperature import reference_temperature as reference_temperature_cls
from .temperature_exponent import temperature_exponent as temperature_exponent_cls

class power_law(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    b: b_cls = ...
    reference_viscosity: reference_viscosity_cls = ...
    reference_temperature: reference_temperature_cls = ...
    temperature_exponent: temperature_exponent_cls = ...
