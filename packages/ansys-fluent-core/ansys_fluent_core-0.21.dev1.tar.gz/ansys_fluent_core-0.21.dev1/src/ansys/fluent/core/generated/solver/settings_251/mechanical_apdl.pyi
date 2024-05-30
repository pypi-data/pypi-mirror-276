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

from .file_name_1 import file_name as file_name_cls
from .thread_name_list import thread_name_list as thread_name_list_cls

class mechanical_apdl(Command):
    fluent_name = ...
    argument_names = ...
    file_name: file_name_cls = ...
    thread_name_list: thread_name_list_cls = ...
