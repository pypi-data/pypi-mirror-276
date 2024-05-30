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

from .method_19 import method as method_cls
from .frequency_6 import frequency as frequency_cls
from .sampling_after import sampling_after as sampling_after_cls

class evaluation(Group):
    fluent_name = ...
    child_names = ...
    method: method_cls = ...
    frequency: frequency_cls = ...
    sampling_after: sampling_after_cls = ...
