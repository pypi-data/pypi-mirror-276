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

from .sc_def_file_settings import sc_def_file_settings as sc_def_file_settings_cls
from .settings import settings as settings_cls
from .abaqus import abaqus as abaqus_cls
from .mechanical_apdl import mechanical_apdl as mechanical_apdl_cls
from .mechanical_apdl_input import mechanical_apdl_input as mechanical_apdl_input_cls
from .custom_heat_flux import custom_heat_flux as custom_heat_flux_cls
from .icemcfd_for_icepak import icemcfd_for_icepak as icemcfd_for_icepak_cls
from .fast_mesh import fast_mesh as fast_mesh_cls
from .fast_solution import fast_solution as fast_solution_cls
from .fast_velocity import fast_velocity as fast_velocity_cls
from .taitherm import taitherm as taitherm_cls

class export(Group):
    fluent_name = ...
    child_names = ...
    sc_def_file_settings: sc_def_file_settings_cls = ...
    settings: settings_cls = ...
    command_names = ...

    def abaqus(self, name: str, surface_name_list: List[str], structural_analysis: bool, write_loads: bool, loads: List[str]):
        """
        Write an ABAQUS file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surface_name_list : typing.List[str]
                'surface_name_list' child.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
        
        """

    def mechanical_apdl(self, name: str, thread_name_list: List[str]):
        """
        Write an Mechanical APDL file.
        
        Parameters
        ----------
            name : str
                'name' child.
            thread_name_list : typing.List[str]
                'thread_name_list' child.
        
        """

    def mechanical_apdl_input(self, name: str, surface_name_list: List[str], structural_analysis: bool, write_loads: bool, loads: List[str]):
        """
        Write an Mechanical APDL Input file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surface_name_list : typing.List[str]
                'surface_name_list' child.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
        
        """

    def custom_heat_flux(self, name: str, wall_function: bool, surface_name_list: List[str]):
        """
        Write a generic file for heat transfer.
        
        Parameters
        ----------
            name : str
                'name' child.
            wall_function : bool
                'wall_function' child.
            surface_name_list : typing.List[str]
                'surface_name_list' child.
        
        """

    def icemcfd_for_icepak(self, name: str):
        """
        Write a binary ICEMCFD domain file.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def fast_mesh(self, name: str):
        """
        Write a FAST/Plot3D unstructured mesh file.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def fast_solution(self, name: str):
        """
        Write a FAST/Plot3D unstructured solution file.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def fast_velocity(self, name: str):
        """
        Write a FAST/Plot3D unstructured vector function file.
        
        Parameters
        ----------
            name : str
                'name' child.
        
        """

    def taitherm(self, name: str, surface_name_list: List[str], wall_function: bool, htc_on_walls: bool):
        """
        Write a TAITherm file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surface_name_list : typing.List[str]
                'surface_name_list' child.
            wall_function : bool
                'wall_function' child.
            htc_on_walls : bool
                'htc_on_walls' child.
        
        """

