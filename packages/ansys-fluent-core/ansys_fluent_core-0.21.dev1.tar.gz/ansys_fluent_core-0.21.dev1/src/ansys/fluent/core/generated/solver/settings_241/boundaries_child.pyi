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

from .name import name as name_cls
from .type_5 import type as type_cls
from .locations import locations as locations_cls

class boundaries_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    type: type_cls = ...
    locations: locations_cls = ...
