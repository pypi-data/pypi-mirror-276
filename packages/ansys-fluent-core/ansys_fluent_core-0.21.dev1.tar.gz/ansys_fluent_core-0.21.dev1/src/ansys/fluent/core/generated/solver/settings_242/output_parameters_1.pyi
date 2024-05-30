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

from .report_definitions_1 import report_definitions as report_definitions_cls
from .named_expressions_1 import named_expressions as named_expressions_cls
from .list_5 import list as list_cls
from .print_all_to_console import print_all_to_console as print_all_to_console_cls
from .write_all_to_file import write_all_to_file as write_all_to_file_cls

class output_parameters(Group):
    fluent_name = ...
    child_names = ...
    report_definitions: report_definitions_cls = ...
    named_expressions: named_expressions_cls = ...
    command_names = ...

    def list(self, ):
        """
        List all output parameters.
        """

    def print_all_to_console(self, ):
        """
        Print all parameters value to console.
        """

    def write_all_to_file(self, file_name: str, append_data: bool):
        """
        Write all parameters value to file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

