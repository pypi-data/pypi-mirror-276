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

from .from_zone_type_1 import from_zone_type as from_zone_type_cls
from .from_zone_name_1 import from_zone_name as from_zone_name_cls
from .phase_59 import phase as phase_cls

class compute_defaults(Command):
    fluent_name = ...
    argument_names = ...
    from_zone_type: from_zone_type_cls = ...
    from_zone_name: from_zone_name_cls = ...
    phase: phase_cls = ...
