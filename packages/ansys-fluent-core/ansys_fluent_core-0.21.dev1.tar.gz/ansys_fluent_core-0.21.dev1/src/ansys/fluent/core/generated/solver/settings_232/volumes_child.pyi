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

from .type_3 import type as type_cls
from .boundaries import boundaries as boundaries_cls
from .locations import locations as locations_cls

class volumes_child(Group):
    fluent_name = ...
    child_names = ...
    type: type_cls = ...
    boundaries: boundaries_cls = ...
    locations: locations_cls = ...
