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

from .option_3 import option as option_cls
from .create_particles_every_dpm_step import create_particles_every_dpm_step as create_particles_every_dpm_step_cls
from .dpm_time_step_size import dpm_time_step_size as dpm_time_step_size_cls
from .number_of_time_steps import number_of_time_steps as number_of_time_steps_cls
from .clear_all_particles import clear_all_particles as clear_all_particles_cls

class unsteady_tracking(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    create_particles_every_dpm_step: create_particles_every_dpm_step_cls = ...
    dpm_time_step_size: dpm_time_step_size_cls = ...
    number_of_time_steps: number_of_time_steps_cls = ...
    command_names = ...

    def clear_all_particles(self, ):
        """
        Clear all particles currently in the domain.
        """

