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

from .start_time import start_time as start_time_cls
from .stop_time import stop_time as stop_time_cls

class times(Group):
    fluent_name = ...
    child_names = ...
    start_time: start_time_cls = ...
    stop_time: stop_time_cls = ...
