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

from .zone_name_1 import zone_name as zone_name_cls
from .growth_rate import growth_rate as growth_rate_cls

class redistribute_boundary_layer(Command):
    fluent_name = ...
    argument_names = ...
    zone_name: zone_name_cls = ...
    growth_rate: growth_rate_cls = ...
