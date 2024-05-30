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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .write_table_1 import write_table as write_table_cls
from .read_table_1 import read_table as read_table_cls
from .print_table_1 import print_table as print_table_cls
from .internal_resistance_table_child import internal_resistance_table_child


class internal_resistance_table(ListObject[internal_resistance_table_child]):
    fluent_name = ...
    command_names = ...

    def list_properties(self, object_at: int):
        """
        List properties of selected object.
        
        Parameters
        ----------
            object_at : int
                Select object index to delete.
        
        """

    def resize(self, size: int):
        """
        Set number of objects for list-object.
        
        Parameters
        ----------
            size : int
                New size for list-object.
        
        """

    def write_table(self, file_name: str):
        """
        Writing 3D table command.
        
        Parameters
        ----------
            file_name : str
                Set file name in the 3D table-writing command.
        
        """

    def read_table(self, file_name_1: str):
        """
        3D Reading table command.
        
        Parameters
        ----------
            file_name_1 : str
                Set file name in the 3D table-reading command.
        
        """

    def print_table(self, ):
        """
        3D table-printing command.
        """

    child_object_type = ...
