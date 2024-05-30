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

from .clear_model import clear_model as clear_model_cls
from .export_model import export_model as export_model_cls
from .import_model import import_model as import_model_cls

class management(Group):
    fluent_name = ...
    command_names = ...

    def clear_model(self, ):
        """
        Initialize the model coefficients.
        """

    def export_model(self, file_name: str):
        """
        Write the model setting and coefficient to a file.
        
        Parameters
        ----------
            file_name : str
                Model data file name.
        
        """

    def import_model(self, file_name: str):
        """
        Read the model setting and coefficients from a file.
        
        Parameters
        ----------
            file_name : str
                Model data file name.
        
        """

