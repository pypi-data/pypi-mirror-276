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

from .adjoint_observable import adjoint_observable as adjoint_observable_cls
from .evaluate import evaluate as evaluate_cls
from .write_to_file_4 import write_to_file as write_to_file_cls

class selection(Group):
    fluent_name = ...
    child_names = ...
    adjoint_observable: adjoint_observable_cls = ...
    command_names = ...

    def evaluate(self, ):
        """
        Evaluate selected observable.
        """

    def write_to_file(self, file_name: str, append_data: bool):
        """
        Write observable to file.
        
        Parameters
        ----------
            file_name : str
                File name.
            append_data : bool
                Append data to file.
        
        """

