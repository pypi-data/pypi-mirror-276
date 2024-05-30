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

from .enable_4 import enable as enable_cls
from .mode import mode as mode_cls
from .disk import disk as disk_cls

class virtual_blade_model(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    mode: mode_cls = ...
    disk: disk_cls = ...
