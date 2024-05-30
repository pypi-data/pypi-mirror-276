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
from .min_val import min_val as min_val_cls

class set_minimum(Command):
    fluent_name = ...
    argument_names = ...
    sample_var: sample_var_cls = ...
    min_val: min_val_cls = ...
