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

from .enable_4 import enable as enable_cls
from .zone_name_5 import zone_name as zone_name_cls

class inlet_temperature_for_operating_density(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    zone_name: zone_name_cls = ...
