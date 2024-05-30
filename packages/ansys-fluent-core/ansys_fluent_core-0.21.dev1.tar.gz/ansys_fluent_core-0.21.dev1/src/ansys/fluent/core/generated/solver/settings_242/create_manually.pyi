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

from .name_2 import name as name_cls
from .zone_list_1 import zone_list_1 as zone_list_1_cls
from .zone_list_2 import zone_list_2 as zone_list_2_cls

class create_manually(Command):
    fluent_name = ...
    argument_names = ...
    name: name_cls = ...
    zone_list_1: zone_list_1_cls = ...
    zone_list_2: zone_list_2_cls = ...
