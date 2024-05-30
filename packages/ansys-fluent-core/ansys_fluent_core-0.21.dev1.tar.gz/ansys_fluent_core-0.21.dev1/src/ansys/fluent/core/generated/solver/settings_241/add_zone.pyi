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

from .zone_name import zone_name as zone_name_cls
from .value_1 import value as value_cls

class add_zone(Command):
    fluent_name = ...
    argument_names = ...
    zone_name: zone_name_cls = ...
    value: value_cls = ...
