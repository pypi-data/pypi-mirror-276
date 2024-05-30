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

from .direction_from_solar_calculator import direction_from_solar_calculator as direction_from_solar_calculator_cls
from .sun_direction_vector import sun_direction_vector as sun_direction_vector_cls

class sun_direction_vector_definition(Group):
    fluent_name = ...
    child_names = ...
    direction_from_solar_calculator: direction_from_solar_calculator_cls = ...
    sun_direction_vector: sun_direction_vector_cls = ...
