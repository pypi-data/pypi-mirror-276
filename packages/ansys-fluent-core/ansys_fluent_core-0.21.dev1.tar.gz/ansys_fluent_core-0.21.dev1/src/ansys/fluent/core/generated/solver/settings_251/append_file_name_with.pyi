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

from .file_suffix_type import file_suffix_type as file_suffix_type_cls
from .file_decimal_digit import file_decimal_digit as file_decimal_digit_cls

class append_file_name_with(Group):
    fluent_name = ...
    child_names = ...
    file_suffix_type: file_suffix_type_cls = ...
    file_decimal_digit: file_decimal_digit_cls = ...
