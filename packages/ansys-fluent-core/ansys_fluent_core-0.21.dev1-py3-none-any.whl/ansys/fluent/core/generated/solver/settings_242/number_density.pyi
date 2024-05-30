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

from .report_type_1 import report_type as report_type_cls
from .surface_list import surface_list as surface_list_cls
from .volume_list import volume_list as volume_list_cls
from .num_dens_func import num_dens_func as num_dens_func_cls
from .dia_upper_limit import dia_upper_limit as dia_upper_limit_cls
from .plot_12 import plot as plot_cls
from .print_5 import print as print_cls
from .histogram_2 import histogram as histogram_cls
from .write_to_file_3 import write_to_file as write_to_file_cls

class number_density(Group):
    fluent_name = ...
    child_names = ...
    report_type: report_type_cls = ...
    surface_list: surface_list_cls = ...
    volume_list: volume_list_cls = ...
    num_dens_func: num_dens_func_cls = ...
    dia_upper_limit: dia_upper_limit_cls = ...
    command_names = ...

    def plot(self, ):
        """
        Plot number density report.
        """

    def print(self, ):
        """
        Print number density report.
        """

    def histogram(self, ):
        """
        Number density histogram.
        """

    def write_to_file(self, file_name: str):
        """
        Write number density report to file.
        
        Parameters
        ----------
            file_name : str
                Enter file name to write number density report.
        
        """

