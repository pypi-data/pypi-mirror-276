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

from .species_mass_flow import species_mass_flow as species_mass_flow_cls
from .element_mass_flow import element_mass_flow as element_mass_flow_cls
from .uds_flow import uds_flow as uds_flow_cls

class flow(Group):
    fluent_name = ...
    command_names = ...

    def species_mass_flow(self, domain: str):
        """
        Print species mass flow rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
        
        """

    def element_mass_flow(self, domain: str):
        """
        Print element mass flow rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
        
        """

    def uds_flow(self, domain: str):
        """
        Print flow rate at boundaries.
        
        Parameters
        ----------
            domain : str
                Select the domain.
        
        """

