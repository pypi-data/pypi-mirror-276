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

from .pulse_mode import pulse_mode as pulse_mode_cls
from .write_2 import write as write_cls

class pulse(Group):
    fluent_name = ...
    child_names = ...
    pulse_mode: pulse_mode_cls = ...
    command_names = ...

    def write(self, object_name: str, write_format: str, file_name: str):
        """
        'write' command.
        
        Parameters
        ----------
            object_name : str
                'object_name' child.
            write_format : str
                'write_format' child.
            file_name : str
                'file_name' child.
        
        """

