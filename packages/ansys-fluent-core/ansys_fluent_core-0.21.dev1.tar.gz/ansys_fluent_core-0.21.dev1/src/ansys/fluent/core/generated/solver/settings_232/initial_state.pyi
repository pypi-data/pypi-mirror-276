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

from .origin import origin as origin_cls
from .orientation import orientation as orientation_cls

class initial_state(Group):
    fluent_name = ...
    child_names = ...
    origin: origin_cls = ...
    orientation: orientation_cls = ...
