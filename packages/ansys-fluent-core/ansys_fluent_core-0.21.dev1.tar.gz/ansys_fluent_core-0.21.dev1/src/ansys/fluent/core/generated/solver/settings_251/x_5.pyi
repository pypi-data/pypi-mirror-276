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

from .label import label as label_cls
from .number_format import number_format as number_format_cls
from .log_scale import log_scale as log_scale_cls
from .auto_range import auto_range as auto_range_cls
from .min import min as min_cls
from .max import max as max_cls
from .show_major_gridlines import show_major_gridlines as show_major_gridlines_cls
from .major_gridlines import major_gridlines as major_gridlines_cls
from .show_minor_gridlines import show_minor_gridlines as show_minor_gridlines_cls
from .minor_gridlines import minor_gridlines as minor_gridlines_cls

class x(Group):
    fluent_name = ...
    child_names = ...
    label: label_cls = ...
    number_format: number_format_cls = ...
    log_scale: log_scale_cls = ...
    auto_range: auto_range_cls = ...
    min: min_cls = ...
    max: max_cls = ...
    show_major_gridlines: show_major_gridlines_cls = ...
    major_gridlines: major_gridlines_cls = ...
    show_minor_gridlines: show_minor_gridlines_cls = ...
    minor_gridlines: minor_gridlines_cls = ...
