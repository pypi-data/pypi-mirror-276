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

from .cell_function_1 import cell_function as cell_function_cls
from .auto_range_2 import auto_range as auto_range_cls
from .minimum_3 import minimum as minimum_cls
from .maximum_3 import maximum as maximum_cls
from .num_divisions import num_divisions as num_divisions_cls
from .zones_7 import zones as zones_cls
from .axes import axes as axes_cls
from .curves import curves as curves_cls
from .print_4 import print as print_cls
from .plot_5 import plot as plot_cls
from .write_3 import write as write_cls
from .get_values import get_values as get_values_cls

class histogram(Group):
    fluent_name = ...
    child_names = ...
    cell_function: cell_function_cls = ...
    auto_range: auto_range_cls = ...
    minimum: minimum_cls = ...
    maximum: maximum_cls = ...
    num_divisions: num_divisions_cls = ...
    zones: zones_cls = ...
    axes: axes_cls = ...
    curves: curves_cls = ...
    command_names = ...

    def print(self, ):
        """
        Print a histogram of a scalar quantity.
        """

    def plot(self, ):
        """
        Plot a histogram of a scalar quantity.
        """

    def write(self, file_name: str):
        """
        Write a histogram of a scalar quantity to a file.
        
        Parameters
        ----------
            file_name : str
                Enter the name you want the file saved with.
        
        """

    query_names = ...

    def get_values(self, ):
        """
        Get a histogram of a scalar quantity.
        """

