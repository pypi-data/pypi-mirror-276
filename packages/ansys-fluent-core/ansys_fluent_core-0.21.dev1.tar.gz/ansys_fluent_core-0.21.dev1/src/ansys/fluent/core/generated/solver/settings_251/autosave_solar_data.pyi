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

from .solar_frequency_data import solar_frequency_data as solar_frequency_data_cls
from .solar_filename import solar_filename as solar_filename_cls
from .use_binary_format import use_binary_format as use_binary_format_cls

class autosave_solar_data(Group):
    fluent_name = ...
    child_names = ...
    solar_frequency_data: solar_frequency_data_cls = ...
    solar_filename: solar_filename_cls = ...
    use_binary_format: use_binary_format_cls = ...
