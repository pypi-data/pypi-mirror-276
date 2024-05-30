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

from .database import database as database_cls
from .fluid import fluid as fluid_cls
from .solid import solid as solid_cls
from .mixture import mixture as mixture_cls
from .inert_particle import inert_particle as inert_particle_cls
from .droplet_particle import droplet_particle as droplet_particle_cls
from .combusting_particle import combusting_particle as combusting_particle_cls
from .particle_mixture import particle_mixture as particle_mixture_cls
from .list_materials_1 import list_materials as list_materials_cls
from .list_properties_1 import list_properties as list_properties_cls

class materials(Group):
    fluent_name = ...
    child_names = ...
    database: database_cls = ...
    fluid: fluid_cls = ...
    solid: solid_cls = ...
    mixture: mixture_cls = ...
    inert_particle: inert_particle_cls = ...
    droplet_particle: droplet_particle_cls = ...
    combusting_particle: combusting_particle_cls = ...
    particle_mixture: particle_mixture_cls = ...
    command_names = ...

    def list_materials(self, ):
        """
        List all locally-stored materials.
        """

    def list_properties(self, name: str):
        """
        List the properties of a locally-stored material.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

