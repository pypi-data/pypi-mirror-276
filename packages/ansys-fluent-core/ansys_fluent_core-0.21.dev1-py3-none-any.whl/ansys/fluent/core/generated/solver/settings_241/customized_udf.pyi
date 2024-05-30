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

from .enabled_14 import enabled as enabled_cls
from .source_file import source_file as source_file_cls
from .create_customized_addon_lib import create_customized_addon_lib as create_customized_addon_lib_cls

class customized_udf(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    source_file: source_file_cls = ...
    command_names = ...

    def create_customized_addon_lib(self, ):
        """
        Compile customized addon library.
        """

