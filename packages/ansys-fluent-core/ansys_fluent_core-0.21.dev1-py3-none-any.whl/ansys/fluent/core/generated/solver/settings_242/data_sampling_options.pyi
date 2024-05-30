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

from .data_sets import data_sets as data_sets_cls
from .add_datasets import add_datasets as add_datasets_cls
from .list_datasets import list_datasets as list_datasets_cls

class data_sampling_options(Group):
    fluent_name = ...
    child_names = ...
    data_sets: data_sets_cls = ...
    command_names = ...

    def add_datasets(self, zone_names: List[str], domain: str, quantities: List[str], min: bool, max: bool, mean: bool, rmse: bool, moving_average: bool, average_over: int):
        """
        Add datasets.
        
        Parameters
        ----------
            zone_names : typing.List[str]
                Select one or more zone names.
            domain : str
                Select the domain.
            quantities : typing.List[str]
                Select one or more quantities.
            min : bool
                Choose whether or not to specify the minimum value of the selected quantity(s) will be collected.
            max : bool
                Choose whether or not to specify the maximum value of the selected quantity(s) will be collected.
            mean : bool
                Choose whether or not to specify the average value of the selected quantity(s) will be computed and collected.
            rmse : bool
                Choose whether or not to specify that the root mean square error of the selected quantity(s) will be computed and collected.
            moving_average : bool
                Choose whether or not to specify an interval for averaging of the computed statistics.
            average_over : int
                Specify the number of iterations (steady simulations) or time steps (transient simulations) that will be used for computing the moving average.
        
        """

    def list_datasets(self, ):
        """
        List dataset.
        """

