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

from .include_current_data_1 import include_current_data as include_current_data_cls
from .training_data_files import training_data_files as training_data_files_cls
from .export_data import export_data as export_data_cls
from .import_data import import_data as import_data_cls
from .remove_1 import remove as remove_cls

class manage_data(Group):
    fluent_name = ...
    child_names = ...
    include_current_data: include_current_data_cls = ...
    training_data_files: training_data_files_cls = ...
    command_names = ...

    def export_data(self, file_name: str):
        """
        Export training data to file.
        
        Parameters
        ----------
            file_name : str
                Training data file name.
        
        """

    def import_data(self, file_name: str):
        """
        Export training data to file.
        
        Parameters
        ----------
            file_name : str
                Training data file name.
        
        """

    def remove(self, files: List[str]):
        """
        Remove a selection of imported training data files.
        
        Parameters
        ----------
            files : typing.List[str]
                List of training data files to remove.
        
        """

