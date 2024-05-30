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

    def plot_sample(self, loaded_samples: str, variable_to_sampled: str, weighting_var: str, correlation_var: str, read_fn: str, overwrite: bool):
        """
        'plot_sample' command.
        
        Parameters
        ----------
            loaded_samples : str
                'loaded_samples' child.
            variable_to_sampled : str
                'variable_to_sampled' child.
            weighting_var : str
                'weighting_var' child.
            correlation_var : str
                'correlation_var' child.
            read_fn : str
                'read_fn' child.
            overwrite : bool
                'overwrite' child.
        
        """

    def write_sample(self, loaded_samples: str, variable_to_sampled: str, weighting_var: str, correlation_var: str, read_fn: str, overwrite: bool):
        """
        'write_sample' command.
        
        Parameters
        ----------
            loaded_samples : str
                'loaded_samples' child.
            variable_to_sampled : str
                'variable_to_sampled' child.
            weighting_var : str
                'weighting_var' child.
            correlation_var : str
                'correlation_var' child.
            read_fn : str
                'read_fn' child.
            overwrite : bool
                'overwrite' child.
        
        """

