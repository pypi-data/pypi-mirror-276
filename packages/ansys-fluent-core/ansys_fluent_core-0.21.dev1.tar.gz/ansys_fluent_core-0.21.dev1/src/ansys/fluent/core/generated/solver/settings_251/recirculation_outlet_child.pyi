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
from .phase_26 import phase as phase_cls
from .recirculation_outlet import recirculation_outlet as recirculation_outlet_cls
from .geometry_3 import geometry as geometry_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls

class recirculation_outlet_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    phase: phase_cls = ...
    recirculation_outlet: recirculation_outlet_cls = ...
    geometry: geometry_cls = ...
    query_names = ...

    def adjacent_cell_zone(self, ):
        """
        Get adjacent cell zone for this face zone.
        """

    def shadow_face_zone(self, ):
        """
        Get shadow zone for this wall zone.
        """

