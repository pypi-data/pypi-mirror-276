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

from .thread_number_method import thread_number_method as thread_number_method_cls
from .fixed_thread_number import fixed_thread_number as fixed_thread_number_cls

class thread_number_control(Group):
    fluent_name = ...
    child_names = ...
    thread_number_method: thread_number_method_cls = ...
    fixed_thread_number: fixed_thread_number_cls = ...
