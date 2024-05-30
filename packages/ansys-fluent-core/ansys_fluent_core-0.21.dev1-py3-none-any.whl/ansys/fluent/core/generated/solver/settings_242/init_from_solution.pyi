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

from .option_22 import option as option_cls
from .init_from_data_file import init_from_data_file as init_from_data_file_cls

class init_from_solution(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    init_from_data_file: init_from_data_file_cls = ...
