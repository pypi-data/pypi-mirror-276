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

from .basis import basis as basis_cls
from .method_1 import method as method_cls
from .surfaces_2 import surfaces as surfaces_cls
from .smoothing import smoothing as smoothing_cls
from .resolution import resolution as resolution_cls
from .separation import separation as separation_cls
from .subdivide import subdivide as subdivide_cls
from .non_participating_zone_temperature import non_participating_zone_temperature as non_participating_zone_temperature_cls

class viewfactor_settings(Group):
    fluent_name = ...
    child_names = ...
    basis: basis_cls = ...
    method: method_cls = ...
    surfaces: surfaces_cls = ...
    smoothing: smoothing_cls = ...
    resolution: resolution_cls = ...
    separation: separation_cls = ...
    subdivide: subdivide_cls = ...
    non_participating_zone_temperature: non_participating_zone_temperature_cls = ...
