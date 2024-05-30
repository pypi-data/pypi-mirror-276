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

from .print_process_statistics import print_process_statistics as print_process_statistics_cls
from .print_system_statistics import print_system_statistics as print_system_statistics_cls
from .print_gpgpu_statistics import print_gpgpu_statistics as print_gpgpu_statistics_cls
from .print_time_statistics import print_time_statistics as print_time_statistics_cls

class system(Group):
    fluent_name = ...
    command_names = ...

    def print_process_statistics(self, ):
        """
        Fluent process information.
        """

    def print_system_statistics(self, ):
        """
        System information.
        """

    def print_gpgpu_statistics(self, ):
        """
        GPGPU information.
        """

    def print_time_statistics(self, ):
        """
        Time usage information.
        """

