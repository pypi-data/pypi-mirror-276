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

from .remove_dataset import remove_dataset as remove_dataset_cls
from .list_datasets import list_datasets as list_datasets_cls

class data_sampling_options(Group):
    fluent_name = ...
    command_names = ...

    def remove_dataset(self, name: str):
        """
        Remove dataset.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def list_datasets(self, ):
        """
        List dataset.
        """

