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

from .method_4 import method as method_cls
from .type_1 import type as type_cls
from .interval_1 import interval as interval_cls
from .frequency_1 import frequency as frequency_cls

class single_session_coupling(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    type: type_cls = ...
    interval: interval_cls = ...
    frequency: frequency_cls = ...
