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

from .plot_sample import plot_sample as plot_sample_cls
from .write_sample import write_sample as write_sample_cls

class plot_write_sample(Group):
    fluent_name = ...
    command_names = ...

    def plot_sample(self, sample: str, variable_to_sample: str, weighting_variable: str, correlation_variable: str, file_name: str):
        """
        'plot_sample' command.
        
        Parameters
        ----------
            sample : str
                'sample' child.
            variable_to_sample : str
                'variable_to_sample' child.
            weighting_variable : str
                'weighting_variable' child.
            correlation_variable : str
                'correlation_variable' child.
            file_name : str
                'file_name' child.
        
        """

    def write_sample(self, sample: str, variable_to_sample: str, weighting_variable: str, correlation_variable: str, file_name: str):
        """
        'write_sample' command.
        
        Parameters
        ----------
            sample : str
                'sample' child.
            variable_to_sample : str
                'variable_to_sample' child.
            weighting_variable : str
                'weighting_variable' child.
            correlation_variable : str
                'correlation_variable' child.
            file_name : str
                'file_name' child.
        
        """

