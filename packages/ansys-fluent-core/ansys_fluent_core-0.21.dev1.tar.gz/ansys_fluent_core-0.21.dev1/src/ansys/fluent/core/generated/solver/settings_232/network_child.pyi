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

from .phase_10 import phase as phase_cls
from .name_2 import name as name_cls

class network_child(Group):
    fluent_name = ...
    child_names = ...
    phase: phase_cls = ...
    name: name_cls = ...
