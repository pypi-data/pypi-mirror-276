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

from .create_output_parameter import create_output_parameter as create_output_parameter_cls

class time_child(Group):
    fluent_name = ...
    command_names = ...

    def create_output_parameter(self, ):
        """
        'create_output_parameter' command.
        """

