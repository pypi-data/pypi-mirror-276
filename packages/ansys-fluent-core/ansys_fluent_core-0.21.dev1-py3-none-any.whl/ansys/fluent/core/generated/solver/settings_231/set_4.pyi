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

from .partition_mask import partition_mask as partition_mask_cls
from .verbosity_9 import verbosity as verbosity_cls
from .time_out import time_out as time_out_cls
from .fast_io import fast_io as fast_io_cls

class set(Group):
    fluent_name = ...
    child_names = ...
    partition_mask: partition_mask_cls = ...
    verbosity: verbosity_cls = ...
    time_out: time_out_cls = ...
    fast_io: fast_io_cls = ...
