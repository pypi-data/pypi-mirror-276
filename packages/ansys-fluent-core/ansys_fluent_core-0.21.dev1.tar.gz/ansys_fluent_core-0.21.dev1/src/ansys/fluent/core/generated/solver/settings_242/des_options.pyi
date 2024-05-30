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

from .all_len_modified import all_len_modified as all_len_modified_cls
from .des_limiter_option import des_limiter_option as des_limiter_option_cls

class des_options(Group):
    fluent_name = ...
    child_names = ...
    all_len_modified: all_len_modified_cls = ...
    des_limiter_option: des_limiter_option_cls = ...
