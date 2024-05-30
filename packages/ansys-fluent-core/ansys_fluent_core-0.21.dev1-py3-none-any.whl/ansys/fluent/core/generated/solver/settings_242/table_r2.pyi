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

from .interp_method import interp_method as interp_method_cls
from .z_value import z_value as z_value_cls
from .column_number import column_number as column_number_cls
from .row_number import row_number as row_number_cls
from .column_value import column_value as column_value_cls
from .row_value import row_value as row_value_cls
from .table_value import table_value as table_value_cls
from .z_label import z_label as z_label_cls
from .column_label import column_label as column_label_cls
from .row_label import row_label as row_label_cls
from .table_label import table_label as table_label_cls
from .write_table import write_table as write_table_cls
from .read_table import read_table as read_table_cls
from .print_table import print_table as print_table_cls

class table_r2(Group):
    fluent_name = ...
    child_names = ...
    interp_method: interp_method_cls = ...
    z_value: z_value_cls = ...
    column_number: column_number_cls = ...
    row_number: row_number_cls = ...
    column_value: column_value_cls = ...
    row_value: row_value_cls = ...
    table_value: table_value_cls = ...
    z_label: z_label_cls = ...
    column_label: column_label_cls = ...
    row_label: row_label_cls = ...
    table_label: table_label_cls = ...
    command_names = ...

    def write_table(self, file_name: str):
        """
        2D table writting command.
        
        Parameters
        ----------
            file_name : str
                File name in 2D table writting.
        
        """

    def read_table(self, file_name_1: str):
        """
        2D table reading command.
        
        Parameters
        ----------
            file_name_1 : str
                File name in 2D table reading.
        
        """

    def print_table(self, ):
        """
        2D table printing command.
        """

