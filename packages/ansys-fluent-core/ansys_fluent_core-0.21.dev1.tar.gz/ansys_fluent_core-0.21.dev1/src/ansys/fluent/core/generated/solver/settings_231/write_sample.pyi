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

from .loaded_samples import loaded_samples as loaded_samples_cls
from .variable_to_sampled import variable_to_sampled as variable_to_sampled_cls
from .weighting_var import weighting_var as weighting_var_cls
from .correlation_var import correlation_var as correlation_var_cls
from .read_fn import read_fn as read_fn_cls
from .overwrite import overwrite as overwrite_cls

class write_sample(Command):
    fluent_name = ...
    argument_names = ...
    loaded_samples: loaded_samples_cls = ...
    variable_to_sampled: variable_to_sampled_cls = ...
    weighting_var: weighting_var_cls = ...
    correlation_var: correlation_var_cls = ...
    read_fn: read_fn_cls = ...
    overwrite: overwrite_cls = ...
