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

from .id_1 import id as id_cls
from .active_2 import active as active_cls
from .parameters_6 import parameters as parameters_cls

class conditions_child(Group):
    fluent_name = ...
    child_names = ...
    id: id_cls = ...
    active: active_cls = ...
    parameters: parameters_cls = ...
