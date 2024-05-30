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

    def abaqus(self, file_name: str, surface_name_list: List[str], structural_analysis: bool, write_loads: bool, loads: List[str]):
        """
        Write an ABAQUS file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surface_name_list : typing.List[str]
                List of surfaces to export.
            structural_analysis : bool
                Choose whether structural analysis or not.
            write_loads : bool
                Choose whether or not to write loads.
            loads : typing.List[str]
                Choose the structural loads type to export.
        
        """

    def mechanical_apdl(self, file_name: str, thread_name_list: List[str]):
        """
        Write an Mechanical APDL file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            thread_name_list : typing.List[str]
                Enter cell zone name list.
        
        """

    def mechanical_apdl_input(self, file_name: str, surface_name_list: List[str], structural_analysis: bool, write_loads: bool, loads: List[str]):
        """
        Write an Mechanical APDL Input file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surface_name_list : typing.List[str]
                Select surface.
            structural_analysis : bool
                Choose whether structural analysis or not.
            write_loads : bool
                Choose whether or not to write loads.
            loads : typing.List[str]
                Choose the structural loads type to export.
        
        """

    def ascii(self, file_name: str, surface_name_list: List[str], delimiter: str, cell_func_domain: List[str], location: str):
        """
        Write an ASCII file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surface_name_list : typing.List[str]
                List of surfaces to export.
            delimiter : str
                Select the delimiter separating the fields.
            cell_func_domain : typing.List[str]
                Select the list of quantities to export.
            location : str
                Select the node or cell-center to export data values.
        
        """

    def avs(self, file_name: str, cell_func_domain_export: List[str]):
        """
        Write an AVS file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            cell_func_domain_export : typing.List[str]
                Select the list of quantities to export.
        
        """

    def ensight(self, file_name: str, cell_func_domain_export: List[str]):
        """
        Write EnSight 6 geometry, velocity, and scalar files.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            cell_func_domain_export : typing.List[str]
                Select the list of quantities to export.
        
        """

    def ensight_gold(self, file_name: str, cell_func_domain_export: List[str], binary_format: bool, cellzones: List[str], interior_zone_surfaces: List[str], cell_centered: bool):
        """
        Write EnSight Gold geometry, velocity, and scalar files.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            cell_func_domain_export : typing.List[str]
                Select the list of quantities to export.
            binary_format : bool
                Choose whether or not to export in binary format.
            cellzones : typing.List[str]
                List of cell zones to export.
            interior_zone_surfaces : typing.List[str]
                List of surfaces to export.
            cell_centered : bool
                Choose whether or not export the cell center data values.
        
        """

    def fieldview(self, file_name: str, cell_func_domain_export: List[str]):
        """
        Write Fieldview case and data files.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            cell_func_domain_export : typing.List[str]
                Select the list of quantities to export.
        
        """

    def fieldview_data(self, file_name: str, cell_func_domain_export: List[str]):
        """
        Write Fieldview case and data files.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            cell_func_domain_export : typing.List[str]
                Select the list of quantities to export.
        
        """

    def gambit(self, file_name: str, cell_func_domain_export: List[str]):
        """
        Write a Gambit neutral file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            cell_func_domain_export : typing.List[str]
                Select the list of quantities to export.
        
        """

    def cgns(self, file_name: str, scope: str, cell_zones: List[str], surfaces: List[str], cell_centered: bool, format_class: str, cgns_scalar: List[str]):
        """
        Write a CGNS file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            scope : str
                Select the scope of the export (volume, surface, full domain).
            cell_zones : typing.List[str]
                Enter cell zone name list.
            surfaces : typing.List[str]
                Select surface.
            cell_centered : bool
                Choose whether or not export the cell center data values.
            format_class : str
                Select the format to export.
            cgns_scalar : typing.List[str]
                Select the list of quantities to export.
        
        """

    def custom_heat_flux(self, file_name: str, wall_function: bool, surface_name_list: List[str]):
        """
        Write a generic file for heat transfer.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            wall_function : bool
                Choose whether or not to include the wall function.
            surface_name_list : typing.List[str]
                Select the list of surfaces to export.
        
        """

    def dx(self, file_name: str, surfaces: List[str], techplot_scalars: List[str]):
        """
        Write an IBM Data Explorer format file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surfaces : typing.List[str]
                Select surface.
            techplot_scalars : typing.List[str]
                Select the list of quantities to export.
        
        """

    def ensight_gold_parallel_surfaces(self, file_name: str, binary_format: bool, surfaces: List[str], cell_centered: bool, cell_function: List[str]):
        """
        Write EnSight Gold geometry, velocity and scalar files for surfaces. Fluent will write files suitable for EnSight Parallel.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            binary_format : bool
                Choose whether or not to export in binary format.
            surfaces : typing.List[str]
                Select surface.
            cell_centered : bool
                Choose whether or not export the cell center data values.
            cell_function : typing.List[str]
                Select the list of quantities to export.
        
        """

    def ensight_gold_parallel_volume(self, file_name: str, binary_format: bool, cellzones: List[str], cell_centered: bool, cell_function: List[str]):
        """
        Write EnSight Gold geometry, velocity and scalar files for cell zones and boundaries attached to them. Fluent will write files suitable for EnSight Parallel.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            binary_format : bool
                Choose whether or not to export in binary format.
            cellzones : typing.List[str]
                Enter cell zone name list.
            cell_centered : bool
                Choose whether or not export the cell center data values.
            cell_function : typing.List[str]
                Select the list of quantities to export.
        
        """

    def icemcfd_for_icepak(self, file_name: str):
        """
        Write a binary ICEMCFD domain file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
        
        """

    def fast_mesh(self, file_name: str):
        """
        Write a FAST/Plot3D unstructured mesh file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
        
        """

    def fast_solution(self, file_name: str):
        """
        Write a FAST/Plot3D unstructured solution file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
        
        """

    def fast_velocity(self, file_name: str):
        """
        Write a FAST/Plot3D unstructured vector function file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
        
        """

    def taitherm(self, file_name: str, surface_name_list: List[str], wall_function: bool, htc_on_walls: bool):
        """
        Write a TAITherm file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surface_name_list : typing.List[str]
                Select surface.
            wall_function : bool
                Choose whether or not to write the heat transfer coefficient from wall function.
            htc_on_walls : bool
                Choose whether or not to write heat transfer coefficient on all the walls.
        
        """

    def fieldview_unstruct(self, file_name: str, surfaces: List[str], cellzones: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured combined file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surfaces : typing.List[str]
                List of surfaces to export.
            cellzones : typing.List[str]
                List of cell zones to export.
            cell_func_domain : typing.List[str]
                Select the list of quantities to export.
        
        """

    def fieldview_unstruct_mesh(self, file_name: str, surfaces: List[str], cellzones: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured mesh only file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surfaces : typing.List[str]
                List of surfaces to export.
            cellzones : typing.List[str]
                List of cell zones to export.
            cell_func_domain : typing.List[str]
                Select the list of quantities to export.
        
        """

    def fieldview_unstruct_data(self, file_name: str, surfaces: List[str], cellzones: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured results only file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surfaces : typing.List[str]
                List of surfaces to export.
            cellzones : typing.List[str]
                List of cell zones to export.
            cell_func_domain : typing.List[str]
                Select the list of quantities to export.
        
        """

    def fieldview_unstruct_surfaces(self, option: str, file_name: str, surfaces: List[str], cell_func_domain: List[str]):
        """
        Write a Fieldview unstructured surface mesh, data.
        
        Parameters
        ----------
            option : str
                Select to export results, mesh or combined.
            file_name : str
                Enter the desired file name to export.
            surfaces : typing.List[str]
                Select surface.
            cell_func_domain : typing.List[str]
                Select the list of quantities to export.
        
        """

    def ideas(self, file_name: str, surfaces: List[str], structural_analysis: bool, write_loads: bool, loads: List[str], cell_func_domain_export: List[str]):
        """
        Write an IDEAS universal file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surfaces : typing.List[str]
                List of surfaces to export.
            structural_analysis : bool
                Choose whether structural analysis or not.
            write_loads : bool
                Choose whether or not to write loads.
            loads : typing.List[str]
                Choose the structural loads type to export.
            cell_func_domain_export : typing.List[str]
                Select the list of quantities to export.
        
        """

    def nastran(self, file_name: str, bndry_threads: List[str], surfaces: List[str], structural_analysis: bool, write_loads: bool, loads: List[str], cell_func_domain_export: List[str]):
        """
        Write a NASTRAN file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            bndry_threads : typing.List[str]
                Enter boundary zone name list.
            surfaces : typing.List[str]
                Select surface.
            structural_analysis : bool
                Choose whether structural analysis or not.
            write_loads : bool
                Choose whether or not to write loads.
            loads : typing.List[str]
                Choose the structural loads type to export.
            cell_func_domain_export : typing.List[str]
                Select the list of quantities to export.
        
        """

    def patran_neutral(self, file_name: str, surfaces: List[str], structural_analysis: bool, write_loads: bool, loads: List[str], cell_func_domain_export: List[str]):
        """
        Write a PATRAN neutral file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surfaces : typing.List[str]
                Select surface.
            structural_analysis : bool
                Choose whether structural analysis or not.
            write_loads : bool
                Choose whether or not to write loads.
            loads : typing.List[str]
                Choose the structural loads type to export.
            cell_func_domain_export : typing.List[str]
                Select the list of quantities to export.
        
        """

    def patran_nodal(self, file_name: str, surfaces: List[str], cell_func_domain_export: List[str]):
        """
        Write a PATRAN nodal results file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surfaces : typing.List[str]
                Select the list of surfaces to export.
            cell_func_domain_export : typing.List[str]
                Select the list of quantities to export.
        
        """

    def tecplot(self, file_name: str, surfaces: List[str], cell_func_domain_export: List[str]):
        """
        Write a Tecplot+3DV format file.
        
        Parameters
        ----------
            file_name : str
                Enter the desired file name to export.
            surfaces : typing.List[str]
                Select surface.
            cell_func_domain_export : typing.List[str]
                Select the list of quantities to export.
        
        """

