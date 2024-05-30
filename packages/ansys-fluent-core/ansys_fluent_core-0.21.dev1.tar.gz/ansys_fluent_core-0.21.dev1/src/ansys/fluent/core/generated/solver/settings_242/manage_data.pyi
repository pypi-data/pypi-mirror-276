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

from .export_sensitivity import export_sensitivity as export_sensitivity_cls
from .import_sensitivity import import_sensitivity as import_sensitivity_cls
from .reload import reload as reload_cls
from .remove import remove as remove_cls
from .reload_all import reload_all as reload_all_cls
from .remove_all import remove_all as remove_all_cls

class manage_data(Group):
    fluent_name = ...
    command_names = ...

    def export_sensitivity(self, file_name: str):
        """
        Write current data sensitivities to file.
        
        Parameters
        ----------
            file_name : str
                Sensitivities file output name.
        
        """

    def import_sensitivity(self, file_name: str):
        """
        Read sensitivities from data file.
        
        Parameters
        ----------
            file_name : str
                Sensitivities file input name.
        
        """

    def reload(self, file_list: List[str]):
        """
        Reload sensitivities from data file.
        
        Parameters
        ----------
            file_list : typing.List[str]
                Sensitivities list to reload.
        
        """

    def remove(self, file_list: List[str]):
        """
        Reload sensitivities from data file.
        
        Parameters
        ----------
            file_list : typing.List[str]
                Sensitivities list to remove.
        
        """

    def reload_all(self, ):
        """
        Reset morphing numerics to default.
        """

    def remove_all(self, ):
        """
        Reset morphing numerics to default.
        """

