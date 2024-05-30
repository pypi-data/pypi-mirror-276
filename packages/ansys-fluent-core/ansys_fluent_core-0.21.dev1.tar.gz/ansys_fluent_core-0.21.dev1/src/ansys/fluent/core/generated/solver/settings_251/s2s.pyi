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

from .viewfactor_settings import viewfactor_settings as viewfactor_settings_cls
from .clustering_settings import clustering_settings as clustering_settings_cls
from .radiosity_solver_control import radiosity_solver_control as radiosity_solver_control_cls
from .compute_write_vf import compute_write_vf as compute_write_vf_cls
from .compute_vf_accelerated import compute_vf_accelerated as compute_vf_accelerated_cls
from .compute_clusters_and_vf_accelerated import compute_clusters_and_vf_accelerated as compute_clusters_and_vf_accelerated_cls
from .compute_vf_only import compute_vf_only as compute_vf_only_cls
from .read_vf_file import read_vf_file as read_vf_file_cls

class s2s(Group):
    fluent_name = ...
    child_names = ...
    viewfactor_settings: viewfactor_settings_cls = ...
    clustering_settings: clustering_settings_cls = ...
    radiosity_solver_control: radiosity_solver_control_cls = ...
    command_names = ...

    def compute_write_vf(self, file_name: str):
        """
        Compute and write both surface clusters and view factors.
        
        Parameters
        ----------
            file_name : str
                Name of output file for updated surface clusters and view factors.
        
        """

    def compute_vf_accelerated(self, file_name: str):
        """
        Compute and write only view factors from existing surface clusters with GPU-acceleration.
        
        Parameters
        ----------
            file_name : str
                Name of output file for S2S view factors from existing surface clusters with GPU-acceleration.
        
        """

    def compute_clusters_and_vf_accelerated(self, file_name: str):
        """
        Compute and write both surface clusters and view factors with GPU-acceleration.
        
        Parameters
        ----------
            file_name : str
                Name of output file for updated surface clusters and view factors with GPU-acceleration.
        
        """

    def compute_vf_only(self, file_name: str):
        """
        Compute and write only view factors from existing surface clusters.
        
        Parameters
        ----------
            file_name : str
                Name of output file for S2S view factors from existing surface clusters.
        
        """

    def read_vf_file(self, file_name_1: str):
        """
        Read an S2S file.
        
        Parameters
        ----------
            file_name_1 : str
                Name of input file containing view factors.
        
        """

