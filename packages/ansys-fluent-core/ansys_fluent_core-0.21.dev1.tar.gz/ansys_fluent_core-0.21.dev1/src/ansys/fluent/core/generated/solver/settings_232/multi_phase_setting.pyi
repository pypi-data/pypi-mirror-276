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

from .enable_12 import enable as enable_cls
from .options_6 import options as options_cls

class multi_phase_setting(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    options: options_cls = ...
