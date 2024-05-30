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

from .change_curr_sample import change_curr_sample as change_curr_sample_cls
from .sample import sample as sample_cls

class pick_sample_to_reduce(Command):
    fluent_name = ...
    argument_names = ...
    change_curr_sample: change_curr_sample_cls = ...
    sample: sample_cls = ...
