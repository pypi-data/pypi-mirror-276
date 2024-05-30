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

from .check_reduction_wt import check_reduction_wt as check_reduction_wt_cls
from .file_name_1 import file_name as file_name_cls
from .overwrite import overwrite as overwrite_cls

class reduce_picked_sample(Command):
    fluent_name = ...
    argument_names = ...
    check_reduction_wt: check_reduction_wt_cls = ...
    file_name: file_name_cls = ...
    overwrite: overwrite_cls = ...
