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

from .sample import sample as sample_cls
from .variable_2 import variable as variable_cls

class compute_sample(Command):
    fluent_name = ...
    argument_names = ...
    sample: sample_cls = ...
    variable: variable_cls = ...
