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

from .recirculation_outlet import recirculation_outlet as recirculation_outlet_cls
from .geometry_3 import geometry as geometry_cls

class phase_child(Group):
    fluent_name = ...
    child_names = ...
    recirculation_outlet: recirculation_outlet_cls = ...
    geometry: geometry_cls = ...
