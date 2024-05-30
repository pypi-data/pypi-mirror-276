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
from .variable_to_sample import variable_to_sample as variable_to_sample_cls
from .weighting_variable import weighting_variable as weighting_variable_cls
from .correlation_variable import correlation_variable as correlation_variable_cls
from .file_name_2 import file_name as file_name_cls

class write_sample(Command):
    fluent_name = ...
    argument_names = ...
    sample: sample_cls = ...
    variable_to_sample: variable_to_sample_cls = ...
    weighting_variable: weighting_variable_cls = ...
    correlation_variable: correlation_variable_cls = ...
    file_name: file_name_cls = ...
