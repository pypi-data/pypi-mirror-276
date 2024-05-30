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

from .zone_names_1 import zone_names as zone_names_cls
from .scale import scale as scale_cls

class scale_zone(Command):
    fluent_name = ...
    argument_names = ...
    zone_names: zone_names_cls = ...
    scale: scale_cls = ...
