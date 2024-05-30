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

from .data_type_4 import data_type as data_type_cls
from .value_9 import value as value_cls
from .profile_4 import profile as profile_cls

class tab_elec_current(Group):
    fluent_name = ...
    child_names = ...
    data_type: data_type_cls = ...
    value: value_cls = ...
    profile: profile_cls = ...
