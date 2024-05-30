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

class anode_fc_zone(Group):
    fluent_name = ...
    child_names = ...
    anode_fc_zone_list: anode_fc_zone_list_cls = ...
