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

from .anode_fc_zone_list import anode_fc_zone_list as anode_fc_zone_list_cls
from .anode_fc_condensation import anode_fc_condensation as anode_fc_condensation_cls
from .anode_fc_evaporation import anode_fc_evaporation as anode_fc_evaporation_cls

class anode_fc_zone(Group):
    fluent_name = ...
    child_names = ...
    anode_fc_zone_list: anode_fc_zone_list_cls = ...
    anode_fc_condensation: anode_fc_condensation_cls = ...
    anode_fc_evaporation: anode_fc_evaporation_cls = ...
