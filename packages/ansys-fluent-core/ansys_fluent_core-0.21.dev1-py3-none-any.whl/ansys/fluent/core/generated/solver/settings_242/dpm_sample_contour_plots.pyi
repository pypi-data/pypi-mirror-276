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

from .sample_name import sample_name as sample_name_cls
from .interval_size import interval_size as interval_size_cls

class dpm_sample_contour_plots(Command):
    fluent_name = ...
    argument_names = ...
    sample_name: sample_name_cls = ...
    interval_size: interval_size_cls = ...
