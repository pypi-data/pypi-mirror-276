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

from .enable_2 import enable as enable_cls
from .components import components as components_cls
from .gravity_mrf_behavior import gravity_mrf_behavior as gravity_mrf_behavior_cls

class gravity(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    components: components_cls = ...
    gravity_mrf_behavior: gravity_mrf_behavior_cls = ...
