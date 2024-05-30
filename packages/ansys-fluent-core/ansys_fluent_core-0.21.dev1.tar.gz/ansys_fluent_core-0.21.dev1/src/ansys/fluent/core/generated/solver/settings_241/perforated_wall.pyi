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

from .setup_method import setup_method as setup_method_cls
from .model_setup import model_setup as model_setup_cls
from .read_input_file import read_input_file as read_input_file_cls

class perforated_wall(Group):
    fluent_name = ...
    child_names = ...
    setup_method: setup_method_cls = ...
    model_setup: model_setup_cls = ...
    command_names = ...

    def read_input_file(self, file_name: str):
        """
        'read_input_file' command.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

