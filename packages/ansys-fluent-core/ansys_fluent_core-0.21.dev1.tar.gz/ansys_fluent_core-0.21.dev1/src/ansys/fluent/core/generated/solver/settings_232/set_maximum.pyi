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
from .max_val import max_val as max_val_cls

class set_maximum(Command):
    fluent_name = ...
    argument_names = ...
    sample_var: sample_var_cls = ...
    max_val: max_val_cls = ...
