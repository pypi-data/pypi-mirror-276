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

from .enabled_19 import enabled as enabled_cls
from .file_name_1_7 import file_name_1 as file_name_1_cls

class read_all_data_table(Command):
    fluent_name = ...
    argument_names = ...
    enabled: enabled_cls = ...
    file_name: file_name_1_cls = ...
