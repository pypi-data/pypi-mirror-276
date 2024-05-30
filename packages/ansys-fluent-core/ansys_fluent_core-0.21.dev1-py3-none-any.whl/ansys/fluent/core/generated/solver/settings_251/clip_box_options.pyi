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

from .selection_type import selection_type as selection_type_cls
from .settings_4 import settings as settings_cls
from .reset import reset as reset_cls

class clip_box_options(Group):
    fluent_name = ...
    child_names = ...
    selection_type: selection_type_cls = ...
    settings: settings_cls = ...
    reset: reset_cls = ...
