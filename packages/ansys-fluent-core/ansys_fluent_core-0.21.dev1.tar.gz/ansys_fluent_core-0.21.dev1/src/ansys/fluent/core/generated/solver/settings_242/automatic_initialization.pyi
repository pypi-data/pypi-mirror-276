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

from .initialization_type_1 import initialization_type as initialization_type_cls
from .data_file_name import data_file_name as data_file_name_cls
from .init_from_solution_1 import init_from_solution as init_from_solution_cls
from .data_file_name2 import data_file_name2 as data_file_name2_cls

class automatic_initialization(Command):
    fluent_name = ...
    argument_names = ...
    initialization_type: initialization_type_cls = ...
    data_file_name: data_file_name_cls = ...
    init_from_solution: init_from_solution_cls = ...
    data_file_name2: data_file_name2_cls = ...
