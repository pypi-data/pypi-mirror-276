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

from .histogram_1 import histogram as histogram_cls
from .sample_trajectories import sample_trajectories as sample_trajectories_cls
from .evap_mass_details_in_dpm_summ_rep import evap_mass_details_in_dpm_summ_rep as evap_mass_details_in_dpm_summ_rep_cls
from .summary import summary as summary_cls
from .extended_summary import extended_summary as extended_summary_cls
from .zone_summaries_per_injection import zone_summaries_per_injection as zone_summaries_per_injection_cls

class discrete_phase(Group):
    fluent_name = ...
    child_names = ...
    histogram: histogram_cls = ...
    sample_trajectories: sample_trajectories_cls = ...
    evap_mass_details_in_dpm_summ_rep: evap_mass_details_in_dpm_summ_rep_cls = ...
    command_names = ...

    def summary(self, ):
        """
        Print discrete phase summary report of particle fates.
        """

    def extended_summary(self, write_to_file: bool, file_name: str, include_in_domains_particles: bool, pick_injection: bool, injection: str):
        """
        Print extended discrete phase summary report of particle fates, with options.
        
        Parameters
        ----------
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            include_in_domains_particles : bool
                'include_in_domains_particles' child.
            pick_injection : bool
                'pick_injection' child.
            injection : str
                'injection' child.
        
        """

    def zone_summaries_per_injection(self, summary_state: bool, reset_dpm_summaries: bool):
        """
        Enable per-injection per-zone DPM summary reports.
        
        Parameters
        ----------
            summary_state : bool
                'summary_state' child.
            reset_dpm_summaries : bool
                'reset_dpm_summaries' child.
        
        """

