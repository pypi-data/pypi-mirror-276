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

from .cathode_fc_zone_list import cathode_fc_zone_list as cathode_fc_zone_list_cls
from .cathode_fc_condensation import cathode_fc_condensation as cathode_fc_condensation_cls
from .cathode_fc_evaporation import cathode_fc_evaporation as cathode_fc_evaporation_cls

class cathode_fc_zone(Group):
    fluent_name = ...
    child_names = ...
    cathode_fc_zone_list: cathode_fc_zone_list_cls = ...
    cathode_fc_condensation: cathode_fc_condensation_cls = ...
    cathode_fc_evaporation: cathode_fc_evaporation_cls = ...
