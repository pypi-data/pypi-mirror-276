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

from .two_stage import two_stage as two_stage_cls
from .default_multi_stage import default_multi_stage as default_multi_stage_cls

class runge_kutta(Group):
    fluent_name = ...
    child_names = ...
    two_stage: two_stage_cls = ...
    default_multi_stage: default_multi_stage_cls = ...
