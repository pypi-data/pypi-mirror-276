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

from .cathode_cc_zone_list import cathode_cc_zone_list as cathode_cc_zone_list_cls
from .cathode_cc_update import cathode_cc_update as cathode_cc_update_cls
from .cathode_cc_material import cathode_cc_material as cathode_cc_material_cls

class cathode_cc_zone(Group):
    fluent_name = ...
    child_names = ...
    cathode_cc_zone_list: cathode_cc_zone_list_cls = ...
    cathode_cc_update: cathode_cc_update_cls = ...
    cathode_cc_material: cathode_cc_material_cls = ...
