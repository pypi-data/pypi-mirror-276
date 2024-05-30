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

from .zone_name_7 import zone_name as zone_name_cls
from .value_4 import value as value_cls

class contact_resis_child(Group):
    fluent_name = ...
    child_names = ...
    zone_name: zone_name_cls = ...
    value: value_cls = ...
