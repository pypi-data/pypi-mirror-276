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

from .frequency_type import frequency_type as frequency_type_cls
from .save_frequency import save_frequency as save_frequency_cls

class save_data_file_every(Group):
    fluent_name = ...
    child_names = ...
    frequency_type: frequency_type_cls = ...
    save_frequency: save_frequency_cls = ...
