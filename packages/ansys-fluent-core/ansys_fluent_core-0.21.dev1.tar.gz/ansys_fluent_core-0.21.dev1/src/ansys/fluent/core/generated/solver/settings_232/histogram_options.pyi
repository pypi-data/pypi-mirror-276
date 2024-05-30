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

from .auto_range_1 import auto_range as auto_range_cls
from .correlation import correlation as correlation_cls
from .cumulation_curve import cumulation_curve as cumulation_curve_cls
from .diameter_statistics import diameter_statistics as diameter_statistics_cls
from .histogram_mode import histogram_mode as histogram_mode_cls
from .percentage import percentage as percentage_cls
from .variable_3 import variable_3 as variable_3_cls
from .logarithmic import logarithmic as logarithmic_cls
from .weighting import weighting as weighting_cls

class histogram_options(Group):
    fluent_name = ...
    child_names = ...
    auto_range: auto_range_cls = ...
    correlation: correlation_cls = ...
    cumulation_curve: cumulation_curve_cls = ...
    diameter_statistics: diameter_statistics_cls = ...
    histogram_mode: histogram_mode_cls = ...
    percentage: percentage_cls = ...
    variable_3: variable_3_cls = ...
    logarithmic: logarithmic_cls = ...
    weighting: weighting_cls = ...
