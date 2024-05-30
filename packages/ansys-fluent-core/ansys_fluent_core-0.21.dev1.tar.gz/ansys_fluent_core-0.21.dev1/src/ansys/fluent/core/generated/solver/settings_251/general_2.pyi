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

from .material_4 import material as material_cls
from .participates_in_radiation import participates_in_radiation as participates_in_radiation_cls
from .glass import glass as glass_cls
from .laminar import laminar as laminar_cls
from .vapor_phase_realgas import vapor_phase_realgas as vapor_phase_realgas_cls
from .active_wetsteam_zone import active_wetsteam_zone as active_wetsteam_zone_cls
from .contact_property import contact_property as contact_property_cls

class general(Group):
    fluent_name = ...
    child_names = ...
    material: material_cls = ...
    participates_in_radiation: participates_in_radiation_cls = ...
    glass: glass_cls = ...
    laminar: laminar_cls = ...
    vapor_phase_realgas: vapor_phase_realgas_cls = ...
    active_wetsteam_zone: active_wetsteam_zone_cls = ...
    contact_property: contact_property_cls = ...
