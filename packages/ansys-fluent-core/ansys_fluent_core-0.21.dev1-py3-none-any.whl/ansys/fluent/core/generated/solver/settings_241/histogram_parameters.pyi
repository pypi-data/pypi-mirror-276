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

from .minimum_val import minimum_val as minimum_val_cls
from .maximum_val import maximum_val as maximum_val_cls
from .number_of_bins import number_of_bins as number_of_bins_cls

class histogram_parameters(Group):
    fluent_name = ...
    child_names = ...
    minimum_val: minimum_val_cls = ...
    maximum_val: maximum_val_cls = ...
    number_of_bins: number_of_bins_cls = ...
