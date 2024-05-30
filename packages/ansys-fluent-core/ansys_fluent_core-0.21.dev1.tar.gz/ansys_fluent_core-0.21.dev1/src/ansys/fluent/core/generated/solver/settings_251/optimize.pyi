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

from .current_warnings import current_warnings as current_warnings_cls
from .disable_settings_validation import disable_settings_validation as disable_settings_validation_cls

class optimize(Command):
    fluent_name = ...
    argument_names = ...
    current_warnings: current_warnings_cls = ...
    disable_settings_validation: disable_settings_validation_cls = ...
