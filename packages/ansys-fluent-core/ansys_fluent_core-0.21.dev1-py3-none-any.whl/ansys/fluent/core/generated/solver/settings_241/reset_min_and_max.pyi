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
from .reset_range import reset_range as reset_range_cls

class reset_min_and_max(Command):
    fluent_name = ...
    argument_names = ...
    sample_var: sample_var_cls = ...
    reset_range: reset_range_cls = ...
