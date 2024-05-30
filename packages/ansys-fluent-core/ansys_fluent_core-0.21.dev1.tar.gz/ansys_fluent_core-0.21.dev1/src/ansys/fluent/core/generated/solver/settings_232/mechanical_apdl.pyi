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

from .name import name as name_cls
from .thread_name_list import thread_name_list as thread_name_list_cls

class mechanical_apdl(Command):
    fluent_name = ...
    argument_names = ...
    name: name_cls = ...
    thread_name_list: thread_name_list_cls = ...
