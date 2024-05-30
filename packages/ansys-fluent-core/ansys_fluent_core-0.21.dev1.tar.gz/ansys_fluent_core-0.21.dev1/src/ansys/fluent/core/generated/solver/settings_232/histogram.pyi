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

from .histogram_options import histogram_options as histogram_options_cls
from .histogram_parameters import histogram_parameters as histogram_parameters_cls
from .plot_write_sample import plot_write_sample as plot_write_sample_cls
from .reduction import reduction as reduction_cls
from .compute_sample import compute_sample as compute_sample_cls
from .delete_sample import delete_sample as delete_sample_cls
from .list_samples import list_samples as list_samples_cls
from .read_sample_file import read_sample_file as read_sample_file_cls
from .dpm_sample_contour_plots import dpm_sample_contour_plots as dpm_sample_contour_plots_cls

class histogram(Group):
    fluent_name = ...
    child_names = ...
    histogram_options: histogram_options_cls = ...
    histogram_parameters: histogram_parameters_cls = ...
    plot_write_sample: plot_write_sample_cls = ...
    reduction: reduction_cls = ...
    command_names = ...

    def compute_sample(self, sample: str, variable: str):
        """
        Compute minimum/maximum of a sample variable.
        
        Parameters
        ----------
            sample : str
                'sample' child.
            variable : str
                'variable' child.
        
        """

    def delete_sample(self, sample: str):
        """
        'delete_sample' command.
        
        Parameters
        ----------
            sample : str
                'sample' child.
        
        """

    def list_samples(self, ):
        """
        Show all samples in loaded sample list.
        """

    def read_sample_file(self, sample_file: str):
        """
        Read a sample file and add it to the sample list.
        
        Parameters
        ----------
            sample_file : str
                Enter the name of a sample file to be loaded.
        
        """

    def dpm_sample_contour_plots(self, sample_name: str, interval_size: Union[float, str]):
        """
        Prepare named expressions from data in a DPM sample file (collected at a cut plane surface) for contour plotting.
        
        Parameters
        ----------
            sample_name : str
                'sample_name' child.
            interval_size : real
                'interval_size' child.
        
        """

