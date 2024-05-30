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

from .expert_4 import expert as expert_cls
from .mixing_plane_model import mixing_plane_model as mixing_plane_model_cls

class general_turbo_interface(Group):
    fluent_name = ...
    child_names = ...
    expert: expert_cls = ...
    mixing_plane_model: mixing_plane_model_cls = ...
