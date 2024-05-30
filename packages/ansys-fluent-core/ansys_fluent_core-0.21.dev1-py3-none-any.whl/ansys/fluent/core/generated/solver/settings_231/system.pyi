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

from .proc_statistics import proc_statistics as proc_statistics_cls
from .sys_statistics import sys_statistics as sys_statistics_cls
from .gpgpu_statistics import gpgpu_statistics as gpgpu_statistics_cls
from .time_statistics import time_statistics as time_statistics_cls

class system(Group):
    fluent_name = ...
    command_names = ...

    def proc_statistics(self, ):
        """
        Fluent process information.
        """

    def sys_statistics(self, ):
        """
        System information.
        """

    def gpgpu_statistics(self, ):
        """
        GPGPU information.
        """

    def time_statistics(self, ):
        """
        Time usage information.
        """

