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

from .file_name_16 import file_name as file_name_cls
from .append_data_1 import append_data as append_data_cls

class write_to_file(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_cls = ...
    append_data: append_data_cls = ...
