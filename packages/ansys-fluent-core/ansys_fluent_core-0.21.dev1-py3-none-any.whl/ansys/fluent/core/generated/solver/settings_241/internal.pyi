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

from .pcb_zone_info import pcb_zone_info as pcb_zone_info_cls
from .pcb_model import pcb_model as pcb_model_cls
from .vapor_phase_realgas import vapor_phase_realgas as vapor_phase_realgas_cls
from .active_wetsteam_zone import active_wetsteam_zone as active_wetsteam_zone_cls
from .contact_property import contact_property as contact_property_cls

class internal(Group):
    fluent_name = ...
    child_names = ...
    pcb_zone_info: pcb_zone_info_cls = ...
    pcb_model: pcb_model_cls = ...
    vapor_phase_realgas: vapor_phase_realgas_cls = ...
    active_wetsteam_zone: active_wetsteam_zone_cls = ...
    contact_property: contact_property_cls = ...
