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

from .enable_turbo_model import enable_turbo_model as enable_turbo_model_cls
from .general_turbo_interface_settings import general_turbo_interface_settings as general_turbo_interface_settings_cls

class turbo_models(Group):
    fluent_name = ...
    child_names = ...
    enable_turbo_model: enable_turbo_model_cls = ...
    general_turbo_interface_settings: general_turbo_interface_settings_cls = ...
