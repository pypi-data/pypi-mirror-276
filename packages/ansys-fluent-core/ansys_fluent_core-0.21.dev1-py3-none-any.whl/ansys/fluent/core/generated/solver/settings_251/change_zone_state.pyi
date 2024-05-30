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

from .zone_name_3 import zone_name as zone_name_cls
from .domain import domain as domain_cls
from .new_phase import new_phase as new_phase_cls

class change_zone_state(Command):
    fluent_name = ...
    argument_names = ...
    zone_name: zone_name_cls = ...
    domain: domain_cls = ...
    new_phase: new_phase_cls = ...
