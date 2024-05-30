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

from .select_sample import select_sample as select_sample_cls
from .plotting_grid_interval_size import plotting_grid_interval_size as plotting_grid_interval_size_cls
from .prepare_expressions import prepare_expressions as prepare_expressions_cls

class dpm_sample_contour_plots(Group):
    fluent_name = ...
    child_names = ...
    select_sample: select_sample_cls = ...
    plotting_grid_interval_size: plotting_grid_interval_size_cls = ...
    command_names = ...

    def prepare_expressions(self, ):
        """
        'prepare_expressions' command.
        """

