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

from .enable_7 import enable as enable_cls
from .mode import mode as mode_cls
from .rotor import rotor as rotor_cls
from .apply import apply as apply_cls

class virtual_blade_model(Group):
    fluent_name = ...
    child_names = ...
    enable: enable_cls = ...
    mode: mode_cls = ...
    rotor: rotor_cls = ...
    command_names = ...

    def apply(self, ):
        """
        Read and apply VBM setting.
        """

