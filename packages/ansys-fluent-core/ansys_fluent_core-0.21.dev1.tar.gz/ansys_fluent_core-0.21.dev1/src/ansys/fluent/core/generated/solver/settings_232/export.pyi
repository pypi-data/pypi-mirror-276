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
from .ascii import ascii as ascii_cls
from .avs import avs as avs_cls
from .ensight import ensight as ensight_cls
from .ensight_gold import ensight_gold as ensight_gold_cls
from .fieldview import fieldview as fieldview_cls
from .fieldview_data import fieldview_data as fieldview_data_cls
from .gambit import gambit as gambit_cls
from .cgns import cgns as cgns_cls
from .custom_heat_flux import custom_heat_flux as custom_heat_flux_cls
from .dx import dx as dx_cls
from .ensight_gold_parallel_surfaces import ensight_gold_parallel_surfaces as ensight_gold_parallel_surfaces_cls
from .ensight_gold_parallel_volume import ensight_gold_parallel_volume as ensight_gold_parallel_volume_cls
from .icemcfd_for_icepak import icemcfd_for_icepak as icemcfd_for_icepak_cls
from .fast_mesh import fast_mesh as fast_mesh_cls
from .fast_solution import fast_solution as fast_solution_cls
from .fast_velocity import fast_velocity as fast_velocity_cls
from .taitherm import taitherm as taitherm_cls
from .fieldview_unstruct import fieldview_unstruct as fieldview_unstruct_cls
from .fieldview_unstruct_mesh import fieldview_unstruct_mesh as fieldview_unstruct_mesh_cls
from .fieldview_unstruct_data import fieldview_unstruct_data as fieldview_unstruct_data_cls
from .fieldview_unstruct_surfaces import fieldview_unstruct_surfaces as fieldview_unstruct_surfaces_cls
from .ideas import ideas as ideas_cls
from .nastran import nastran as nastran_cls
from .patran_neutral import patran_neutral as patran_neutral_cls
from .patran_nodal import patran_nodal as patran_nodal_cls
from .tecplot import tecplot as tecplot_cls

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

    def ascii(self, name: str, surface_name_list: List[str], delimiter: str, cell_func_domain: List[str], location: str):
        """
        Write an ASCII file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surface_name_list : typing.List[str]
                List of surfaces to export.
            delimiter : str
                'delimiter' child.
            cell_func_domain : typing.List[str]
                'cell_func_domain' child.
            location : str
                'location' child.
        
        """

    def avs(self, name: str, cell_func_domain_export: List[str]):
        """
        Write an AVS UCD file.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def ensight(self, name: str, cell_func_domain_export: List[str]):
        """
        Write EnSight 6 geometry, velocity, and scalar files.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def ensight_gold(self, name: str, cell_func_domain_export: List[str]):
        """
        Write EnSight Gold geometry, velocity, and scalar files.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def fieldview(self, name: str, cell_func_domain_export: List[str]):
        """
        Write Fieldview case and data files.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def fieldview_data(self, name: str, cell_func_domain_export: List[str]):
        """
        Write Fieldview case and data files.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def gambit(self, name: str, cell_func_domain_export: List[str]):
        """
        Write a Gambit neutral file.
        
        Parameters
        ----------
            name : str
                'name' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def cgns(self, name: str, scope: str, cell_zones: List[str], surfaces: List[str], cell_centered: bool, format_class: str, cgns_scalar: List[str]):
        """
        Write a CGNS file.
        
        Parameters
        ----------
            name : str
                'name' child.
            scope : str
                'scope' child.
            cell_zones : typing.List[str]
                'cell_zones' child.
            surfaces : typing.List[str]
                'surfaces' child.
            cell_centered : bool
                'cell_centered' child.
            format_class : str
                'format_class' child.
            cgns_scalar : typing.List[str]
                'cgns_scalar' child.
        
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

    def dx(self, name: str, surfaces: List[str], techplot_scalars: List[str]):
        """
        Write an IBM Data Explorer format file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : typing.List[str]
                'surfaces' child.
            techplot_scalars : typing.List[str]
                'techplot_scalars' child.
        
        """

    def ensight_gold_parallel_surfaces(self, name: str, binary_format: bool, surfaces: List[str], cell_centered: bool, cell_function: List[str]):
        """
        Write EnSight Gold geometry, velocity and scalar files for surfaces. Fluent will write files suitable for EnSight Parallel.
        
        Parameters
        ----------
            name : str
                'name' child.
            binary_format : bool
                'binary_format' child.
            surfaces : typing.List[str]
                'surfaces' child.
            cell_centered : bool
                'cell_centered' child.
            cell_function : typing.List[str]
                'cell_function' child.
        
        """

    def ensight_gold_parallel_volume(self, name: str, binary_format: bool, cellzones: List[str], cell_centered: bool, cell_function: List[str]):
        """
        Write EnSight Gold geometry, velocity and scalar files for cell zones and boundaries attached to them. Fluent will write files suitable for EnSight Parallel.
        
        Parameters
        ----------
            name : str
                'name' child.
            binary_format : bool
                'binary_format' child.
            cellzones : typing.List[str]
                'cellzones' child.
            cell_centered : bool
                'cell_centered' child.
            cell_function : typing.List[str]
                'cell_function' child.
        
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

    def fieldview_unstruct(self, name: str, surfaces: List[str], cellzones: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured combined file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : typing.List[str]
                List of surfaces to export.
            cellzones : typing.List[str]
                List of cell zones to export.
            cell_func_domain : typing.List[str]
                'cell_func_domain' child.
        
        """

    def fieldview_unstruct_mesh(self, name: str, surfaces: List[str], cellzones: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured mesh only file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : typing.List[str]
                List of surfaces to export.
            cellzones : typing.List[str]
                List of cell zones to export.
            cell_func_domain : typing.List[str]
                'cell_func_domain' child.
        
        """

    def fieldview_unstruct_data(self, name: str, surfaces: List[str], cellzones: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured results only file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : typing.List[str]
                List of surfaces to export.
            cellzones : typing.List[str]
                List of cell zones to export.
            cell_func_domain : typing.List[str]
                'cell_func_domain' child.
        
        """

    def fieldview_unstruct_surfaces(self, options: str, name: str, surfaces: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured surface mesh, data.
        
        Parameters
        ----------
            options : str
                'options' child.
            name : str
                'name' child.
            surfaces : typing.List[str]
                'surfaces' child.
            cell_func_domain : typing.List[str]
                'cell_func_domain' child.
        
        """

    def ideas(self, name: str, surfaces: List[str], structural_analysis: bool, write_loads: bool, loads: List[str], cell_func_domain_export: List[str]):
        """
        Write an IDEAS universal file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : typing.List[str]
                List of surfaces to export.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def nastran(self, name: str, bndry_threads: List[str], surfaces: List[str], structural_analysis: bool, write_loads: bool, loads: List[str], cell_func_domain_export: List[str]):
        """
        Write a NASTRAN file.
        
        Parameters
        ----------
            name : str
                'name' child.
            bndry_threads : typing.List[str]
                'bndry_threads' child.
            surfaces : typing.List[str]
                'surfaces' child.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def patran_neutral(self, name: str, surfaces: List[str], structural_analysis: bool, write_loads: bool, loads: List[str], cell_func_domain_export: List[str]):
        """
        Write a PATRAN neutral file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : typing.List[str]
                'surfaces' child.
            structural_analysis : bool
                'structural_analysis' child.
            write_loads : bool
                'write_loads' child.
            loads : typing.List[str]
                'loads' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def patran_nodal(self, name: str, surfaces: List[str], cell_func_domain_export: List[str]):
        """
        Write a PATRAN nodal results file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : typing.List[str]
                'surfaces' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

    def tecplot(self, name: str, surfaces: List[str], cell_func_domain_export: List[str]):
        """
        Write a Tecplot+3DV format file.
        
        Parameters
        ----------
            name : str
                'name' child.
            surfaces : typing.List[str]
                'surfaces' child.
            cell_func_domain_export : typing.List[str]
                'cell_func_domain_export' child.
        
        """

