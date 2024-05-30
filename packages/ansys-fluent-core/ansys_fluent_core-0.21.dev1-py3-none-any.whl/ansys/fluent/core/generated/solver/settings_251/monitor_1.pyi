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

from .residual import residual as residual_cls
from .report_files import report_files as report_files_cls
from .report_plots import report_plots as report_plots_cls
from .convergence_conditions import convergence_conditions as convergence_conditions_cls

class monitor(Group):
    fluent_name = ...
    child_names = ...
    residual: residual_cls = ...
    report_files: report_files_cls = ...
    report_plots: report_plots_cls = ...
    convergence_conditions: convergence_conditions_cls = ...
