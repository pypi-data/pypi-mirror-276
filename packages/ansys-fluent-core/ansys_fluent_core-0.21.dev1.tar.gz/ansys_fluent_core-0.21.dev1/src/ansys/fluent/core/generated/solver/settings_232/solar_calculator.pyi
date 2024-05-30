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

from .latitude import latitude as latitude_cls
from .longitude import longitude as longitude_cls
from .timezone import timezone as timezone_cls
from .north_direction import north_direction as north_direction_cls
from .east_direction import east_direction as east_direction_cls
from .date_and_time import date_and_time as date_and_time_cls
from .calculator_method import calculator_method as calculator_method_cls
from .sunshine_factor import sunshine_factor as sunshine_factor_cls

class solar_calculator(Group):
    fluent_name = ...
    child_names = ...
    latitude: latitude_cls = ...
    longitude: longitude_cls = ...
    timezone: timezone_cls = ...
    north_direction: north_direction_cls = ...
    east_direction: east_direction_cls = ...
    date_and_time: date_and_time_cls = ...
    calculator_method: calculator_method_cls = ...
    sunshine_factor: sunshine_factor_cls = ...
