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

from .anode_cc_zone_list import anode_cc_zone_list as anode_cc_zone_list_cls
from .anode_cc_update import anode_cc_update as anode_cc_update_cls
from .anode_cc_material import anode_cc_material as anode_cc_material_cls

class anode_cc_zone(Group):
    fluent_name = ...
    child_names = ...
    anode_cc_zone_list: anode_cc_zone_list_cls = ...
    anode_cc_update: anode_cc_update_cls = ...
    anode_cc_material: anode_cc_material_cls = ...
