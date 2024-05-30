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

from .option import option as option_cls
from .direction_vector_2 import direction_vector as direction_vector_cls
from .curve_length import curve_length as curve_length_cls

class plot_direction(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    direction_vector: direction_vector_cls = ...
    curve_length: curve_length_cls = ...
