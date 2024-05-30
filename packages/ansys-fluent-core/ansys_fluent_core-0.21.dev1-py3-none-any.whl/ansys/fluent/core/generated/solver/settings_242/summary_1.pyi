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

from .write_to_file_1 import write_to_file as write_to_file_cls
from .file_name_2 import file_name as file_name_cls

class summary(Command):
    fluent_name = ...
    argument_names = ...
    write_to_file: write_to_file_cls = ...
    file_name: file_name_cls = ...
