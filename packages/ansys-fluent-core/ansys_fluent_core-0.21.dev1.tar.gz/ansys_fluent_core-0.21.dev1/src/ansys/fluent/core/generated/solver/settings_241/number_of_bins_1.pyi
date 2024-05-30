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

from .sample_var import sample_var as sample_var_cls
from .num_bins import num_bins as num_bins_cls

class number_of_bins(Command):
    fluent_name = ...
    argument_names = ...
    sample_var: sample_var_cls = ...
    num_bins: num_bins_cls = ...
