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

from .cathode_pl_zone_list import cathode_pl_zone_list as cathode_pl_zone_list_cls
from .cathode_pl_update import cathode_pl_update as cathode_pl_update_cls
from .cathode_pl_material import cathode_pl_material as cathode_pl_material_cls
from .cathode_pl_porosity import cathode_pl_porosity as cathode_pl_porosity_cls
from .cathode_pl_kr import cathode_pl_kr as cathode_pl_kr_cls

class cathode_pl_zone(Group):
    fluent_name = ...
    child_names = ...
    cathode_pl_zone_list: cathode_pl_zone_list_cls = ...
    cathode_pl_update: cathode_pl_update_cls = ...
    cathode_pl_material: cathode_pl_material_cls = ...
    cathode_pl_porosity: cathode_pl_porosity_cls = ...
    cathode_pl_kr: cathode_pl_kr_cls = ...
