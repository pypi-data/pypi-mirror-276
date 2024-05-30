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

from .create_zones_from_ccl import create_zones_from_ccl as create_zones_from_ccl_cls
from .read import read as read_cls
from .chemkin_report_each_line import chemkin_report_each_line as chemkin_report_each_line_cls
from .import_fmu import import_fmu as import_fmu_cls

class import_(Group):
    fluent_name = ...
    child_names = ...
    create_zones_from_ccl: create_zones_from_ccl_cls = ...
    command_names = ...

    def read(self, file_type: str, file_name_1: str):
        """
        Allows you to select the file type and import the file.
        
        Parameters
        ----------
            file_type : str
                Select the file type.
            file_name_1 : str
                Specify the name of the file to be read.
        
        """

    def chemkin_report_each_line(self, report_each_line: bool):
        """
        Choose whether or not to report after reading each line.
        
        Parameters
        ----------
            report_each_line : bool
                Enable/disable reporting after reading each line.
        
        """

    def import_fmu(self, file_name_1: str):
        """
        Import a FMU file.
        
        Parameters
        ----------
            file_name_1 : str
                Allows you to import FMU file.
        
        """

