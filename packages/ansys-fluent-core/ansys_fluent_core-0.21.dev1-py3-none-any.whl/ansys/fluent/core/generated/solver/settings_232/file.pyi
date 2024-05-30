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

from .single_precision_coordinates import single_precision_coordinates as single_precision_coordinates_cls
from .binary_legacy_files import binary_legacy_files as binary_legacy_files_cls
from .cff_files import cff_files as cff_files_cls
from .convert_hanging_nodes_during_read import convert_hanging_nodes_during_read as convert_hanging_nodes_during_read_cls
from .async_optimize import async_optimize as async_optimize_cls
from .write_pdat import write_pdat as write_pdat_cls
from .confirm_overwrite import confirm_overwrite as confirm_overwrite_cls
from .auto_save import auto_save as auto_save_cls
from .export import export as export_cls
from .import_ import import_ as import__cls
from .parametric_project import parametric_project as parametric_project_cls
from .cffio_options import cffio_options as cffio_options_cls
from .define_macro import define_macro as define_macro_cls
from .execute_macro import execute_macro as execute_macro_cls
from .read_macros import read_macros as read_macros_cls
from .read_1 import read as read_cls
from .read_case import read_case as read_case_cls
from .read_case_data import read_case_data as read_case_data_cls
from .read_case_setting import read_case_setting as read_case_setting_cls
from .read_data import read_data as read_data_cls
from .read_mesh import read_mesh as read_mesh_cls
from .read_journal import read_journal as read_journal_cls
from .start_journal import start_journal as start_journal_cls
from .stop_journal import stop_journal as stop_journal_cls
from .replace_mesh import replace_mesh as replace_mesh_cls
from .write import write as write_cls
from .read_settings import read_settings as read_settings_cls
from .read_field_functions import read_field_functions as read_field_functions_cls
from .read_injections import read_injections as read_injections_cls
from .read_profile import read_profile as read_profile_cls
from .read_pdf import read_pdf as read_pdf_cls
from .read_isat_table import read_isat_table as read_isat_table_cls
from .show_configuration import show_configuration as show_configuration_cls
from .stop_macro import stop_macro as stop_macro_cls
from .start_transcript import start_transcript as start_transcript_cls
from .stop_transcript import stop_transcript as stop_transcript_cls
from .data_file_options import data_file_options as data_file_options_cls

class file(Group):
    fluent_name = ...
    child_names = ...
    single_precision_coordinates: single_precision_coordinates_cls = ...
    binary_legacy_files: binary_legacy_files_cls = ...
    cff_files: cff_files_cls = ...
    convert_hanging_nodes_during_read: convert_hanging_nodes_during_read_cls = ...
    async_optimize: async_optimize_cls = ...
    write_pdat: write_pdat_cls = ...
    confirm_overwrite: confirm_overwrite_cls = ...
    auto_save: auto_save_cls = ...
    export: export_cls = ...
    import_: import__cls = ...
    parametric_project: parametric_project_cls = ...
    cffio_options: cffio_options_cls = ...
    command_names = ...

    def define_macro(self, filename: str):
        """
        Save input to a named macro.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        
        """

    def execute_macro(self, macro_filename: str):
        """
        Run a previously defined macro.
        
        Parameters
        ----------
            macro_filename : str
                'macro_filename' child.
        
        """

    def read_macros(self, file_name: str):
        """
        Read macro definitions from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_case(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_case' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_case_data(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_case_data' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_case_setting(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_case_setting' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_data(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_data' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_mesh(self, file_type: str, file_name: str, pdf_file_name: str, lightweight_setup: bool):
        """
        'read_mesh' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
            pdf_file_name : str
                'pdf_file_name' child.
            lightweight_setup : bool
                'lightweight_setup' child.
        
        """

    def read_journal(self, file_name_list: List[str]):
        """
        Read a journal file.
        
        Parameters
        ----------
            file_name_list : typing.List[str]
                'file_name_list' child.
        
        """

    def start_journal(self, file_name: str):
        """
        Start recording all input in a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def stop_journal(self, ):
        """
        Stop recording input and close the journal file.
        """

    def replace_mesh(self, file_name: str):
        """
        'replace_mesh' command.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def write(self, file_type: str, file_name: str):
        """
        'write' command.
        
        Parameters
        ----------
            file_type : str
                'file_type' child.
            file_name : str
                'file_name' child.
        
        """

    def read_settings(self, file_name: str):
        """
        Read and set boundary conditions from specified file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_field_functions(self, file_name: str):
        """
        Read custom field-function definitions from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_injections(self, file_name: str):
        """
        Read all DPM injections from a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_profile(self, file_name: str):
        """
        Read boundary profile data (*.prof, *.csv). Default is *.prof.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_pdf(self, file_name: str):
        """
        Read a PDF file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def read_isat_table(self, file_name: str):
        """
        Read an ISAT table.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def show_configuration(self, ):
        """
        Display current release and version information.
        """

    def stop_macro(self, ):
        """
        Stop recording input to a macro.
        """

    def start_transcript(self, file_name: str):
        """
        Start recording input and output in a file.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def stop_transcript(self, ):
        """
        Stop recording input and output and close the transcript file.
        """

    def data_file_options(self, reset_defined_derived_quantities: bool, derived_quantities: List[str]):
        """
        Set derived quantities to be written in data file.
        
        Parameters
        ----------
            reset_defined_derived_quantities : bool
                'reset_defined_derived_quantities' child.
            derived_quantities : typing.List[str]
                'derived_quantities' child.
        
        """

