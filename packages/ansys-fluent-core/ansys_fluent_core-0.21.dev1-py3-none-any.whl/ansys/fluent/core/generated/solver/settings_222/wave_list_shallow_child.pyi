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

from .theory import theory as theory_cls
from .wave_ht import wave_ht as wave_ht_cls
from .wave_len import wave_len as wave_len_cls
from .offset import offset as offset_cls
from .heading_angle import heading_angle as heading_angle_cls

class wave_list_shallow_child(Group):
    fluent_name = ...
    child_names = ...
    theory: theory_cls = ...
    wave_ht: wave_ht_cls = ...
    wave_len: wave_len_cls = ...
    offset: offset_cls = ...
    heading_angle: heading_angle_cls = ...
