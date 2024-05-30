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

from .file_name_17 import file_name as file_name_cls
from .frequency_5 import frequency as frequency_cls
from .max_files_1 import max_files as max_files_cls

class autosave(Group):
    fluent_name = ...
    child_names = ...
    file_name: file_name_cls = ...
    frequency: frequency_cls = ...
    max_files: max_files_cls = ...
