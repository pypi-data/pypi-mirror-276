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

from .area_1 import area as area_cls
from .area_weighted_avg import area_weighted_avg as area_weighted_avg_cls
from .vector_based_flux import vector_based_flux as vector_based_flux_cls
from .vector_flux import vector_flux as vector_flux_cls
from .vector_weighted_average import vector_weighted_average as vector_weighted_average_cls
from .facet_avg import facet_avg as facet_avg_cls
from .facet_min import facet_min as facet_min_cls
from .facet_max import facet_max as facet_max_cls
from .flow_rate_1 import flow_rate as flow_rate_cls
from .integral import integral as integral_cls
from .mass_flow_rate_4 import mass_flow_rate as mass_flow_rate_cls
from .mass_weighted_avg import mass_weighted_avg as mass_weighted_avg_cls
from .standard_deviation import standard_deviation as standard_deviation_cls
from .sum import sum as sum_cls
from .uniformity_index_area_weighted import uniformity_index_area_weighted as uniformity_index_area_weighted_cls
from .uniformity_index_mass_weighted import uniformity_index_mass_weighted as uniformity_index_mass_weighted_cls
from .vertex_avg import vertex_avg as vertex_avg_cls
from .vertex_min import vertex_min as vertex_min_cls
from .vertex_max import vertex_max as vertex_max_cls
from .volume_flow_rate import volume_flow_rate as volume_flow_rate_cls

class surface_integrals(Group):
    fluent_name = ...
    command_names = ...

    def area(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print total area of surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def area_weighted_avg(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print area-weighted average of scalar on surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vector_based_flux(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print custom vector based flux.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vector_flux(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print custom vector flux.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vector_weighted_average(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print custom vector weighted average.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def facet_avg(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print average of scalar at facet centroids of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def facet_min(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print minimum of scalar at facet centroids of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def facet_max(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print maximum of scalar at facet centroids of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def flow_rate(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print flow rate of scalar through surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def integral(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print integral of scalar over surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def mass_flow_rate(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass flow rate through surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def mass_weighted_avg(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print mass-average of scalar over surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def standard_deviation(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print standard deviation of scalar.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def sum(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print sum of scalar at facet centroids of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def uniformity_index_area_weighted(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print uniformity index of scalar over surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def uniformity_index_mass_weighted(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print uniformity index of scalar over surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vertex_avg(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print average of scalar at vertices of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vertex_min(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print minimum of scalar at vertices of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def vertex_max(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print maximkum of scalar at vertices of the surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

    def volume_flow_rate(self, surface_names: List[str], geometry_names: List[str], cust_vec_func: str, report_of: str, current_domain: str, write_to_file: bool, file_name: str, append_data: bool):
        """
        Print volume flow rate through surfaces.
        
        Parameters
        ----------
            surface_names : typing.List[str]
                Select surface.
            geometry_names : typing.List[str]
                Select UTL Geometry.
            cust_vec_func : str
                'cust_vec_func' child.
            report_of : str
                Specify Field.
            current_domain : str
                'current_domain' child.
            write_to_file : bool
                'write_to_file' child.
            file_name : str
                'file_name' child.
            append_data : bool
                'append_data' child.
        
        """

