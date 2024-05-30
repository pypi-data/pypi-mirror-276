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

from .print_histogram import print_histogram as print_histogram_cls
from .write_histogram import write_histogram as write_histogram_cls

class print_write_histogram(Group):
    fluent_name = ...
    command_names = ...

    def print_histogram(self, domain: str, cell_function: str, min_val: Union[float, str], max_val: Union[float, str], num_division: int, set_all_zones: bool, threads_list: List[str], file_name: str, overwrite: bool):
        """
        Print a histogram of a scalar quantity.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            cell_function : str
                'cell_function' child.
            min_val : real
                'min_val' child.
            max_val : real
                'max_val' child.
            num_division : int
                'num_division' child.
            set_all_zones : bool
                'set_all_zones' child.
            threads_list : typing.List[str]
                'threads_list' child.
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def write_histogram(self, domain: str, cell_function: str, min_val: Union[float, str], max_val: Union[float, str], num_division: int, set_all_zones: bool, threads_list: List[str], file_name: str, overwrite: bool):
        """
        Write a histogram of a scalar quantity to a file.
        
        Parameters
        ----------
            domain : str
                'domain' child.
            cell_function : str
                'cell_function' child.
            min_val : real
                'min_val' child.
            max_val : real
                'max_val' child.
            num_division : int
                'num_division' child.
            set_all_zones : bool
                'set_all_zones' child.
            threads_list : typing.List[str]
                'threads_list' child.
            file_name : str
                'file_name' child.
            overwrite : bool
                'overwrite' child.
        
        """

