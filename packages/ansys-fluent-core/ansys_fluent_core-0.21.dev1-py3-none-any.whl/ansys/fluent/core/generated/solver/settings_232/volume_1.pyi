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

from .option import option as option_cls
from .volume_magnitude import volume_magnitude as volume_magnitude_cls
from .volume_change import volume_change as volume_change_cls

class volume(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    volume_magnitude: volume_magnitude_cls = ...
    volume_change: volume_change_cls = ...
