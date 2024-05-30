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

from .list_simulation_reports import list_simulation_reports as list_simulation_reports_cls
from .add_histogram_to_report import add_histogram_to_report as add_histogram_to_report_cls
from .generate_simulation_report import generate_simulation_report as generate_simulation_report_cls
from .view_simulation_report import view_simulation_report as view_simulation_report_cls
from .export_simulation_report_as_pdf import export_simulation_report_as_pdf as export_simulation_report_as_pdf_cls
from .export_simulation_report_as_html import export_simulation_report_as_html as export_simulation_report_as_html_cls
from .export_simulation_report_as_pptx import export_simulation_report_as_pptx as export_simulation_report_as_pptx_cls
from .write_simulation_report_names_to_file import write_simulation_report_names_to_file as write_simulation_report_names_to_file_cls
from .rename_simulation_report import rename_simulation_report as rename_simulation_report_cls
from .duplicate_simulation_report import duplicate_simulation_report as duplicate_simulation_report_cls
from .reset_report_to_defaults import reset_report_to_defaults as reset_report_to_defaults_cls
from .delete_simulation_report import delete_simulation_report as delete_simulation_report_cls
from .write_simulation_report_template_file import write_simulation_report_template_file as write_simulation_report_template_file_cls
from .read_simulation_report_template_file import read_simulation_report_template_file as read_simulation_report_template_file_cls

class simulation_reports(Group):
    fluent_name = ...
    command_names = ...

    def list_simulation_reports(self, ):
        """
        List all report names.
        """

    def add_histogram_to_report(self, ):
        """
        Add a histogram to the current simulation report.
        """

    def generate_simulation_report(self, report_name: str):
        """
        Generate a new simulation report or regenerate an existing simulation report with the provided name.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        
        """

    def view_simulation_report(self, report_name: str):
        """
        View a simulation report that has already been generated. In batch mode this will print the report's URL.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        
        """

    def export_simulation_report_as_pdf(self, report_name: str, file_name: str):
        """
        Export the provided simulation report as a PDF file.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            file_name : str
                'file_name' child.
        
        """

    def export_simulation_report_as_html(self, report_name: str, output_dir: str):
        """
        Export the provided simulation report as HTML.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            output_dir : str
                'output_dir' child.
        
        """

    def export_simulation_report_as_pptx(self, report_name: str, file_name: str):
        """
        Export the provided simulation report as a PPT file.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            file_name : str
                'file_name' child.
        
        """

    def write_simulation_report_names_to_file(self, file_name: str):
        """
        Write the list of currently generated report names to a txt file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def rename_simulation_report(self, report_name: str, new_report_name: str):
        """
        Rename a report which has already been generated.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
            new_report_name : str
                'new_report_name' child.
        
        """

    def duplicate_simulation_report(self, report_name: str):
        """
        Duplicate a report and all of its settings to a new report.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        
        """

    def reset_report_to_defaults(self, report_name: str):
        """
        Reset all report settings to default for the provided simulation report.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        
        """

    def delete_simulation_report(self, report_name: str):
        """
        Delete the provided simulation report.
        
        Parameters
        ----------
            report_name : str
                'report_name' child.
        
        """

    def write_simulation_report_template_file(self, file_name: str):
        """
        Write a JSON template file with this case's Simulation Report settings.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_simulation_report_template_file(self, file_name: str):
        """
        Read a JSON template file with existing Simulation Report settings.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

