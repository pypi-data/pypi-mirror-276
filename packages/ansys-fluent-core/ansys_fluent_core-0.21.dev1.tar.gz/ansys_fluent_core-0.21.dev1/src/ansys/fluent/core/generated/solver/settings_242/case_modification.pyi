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

from .before_init_modification import before_init_modification as before_init_modification_cls
from .original_settings import original_settings as original_settings_cls
from .modifications import modifications as modifications_cls

class case_modification(Group):
    fluent_name = ...
    child_names = ...
    before_init_modification: before_init_modification_cls = ...
    original_settings: original_settings_cls = ...
    modifications: modifications_cls = ...
