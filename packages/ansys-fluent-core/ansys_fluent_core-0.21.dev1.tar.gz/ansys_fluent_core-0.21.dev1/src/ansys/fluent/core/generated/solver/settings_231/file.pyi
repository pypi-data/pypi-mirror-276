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
from .async_optimize import async_optimize as async_optimize_cls
from .write_pdat import write_pdat as write_pdat_cls
from .confirm_overwrite import confirm_overwrite as confirm_overwrite_cls
from .export import export as export_cls
from .import_ import import_ as import__cls
from .parametric_project import parametric_project as parametric_project_cls
from .auto_save import auto_save as auto_save_cls
from .define_macro import define_macro as define_macro_cls
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

class file(Group):
    fluent_name = ...
    child_names = ...
    single_precision_coordinates: single_precision_coordinates_cls = ...
    binary_legacy_files: binary_legacy_files_cls = ...
    cff_files: cff_files_cls = ...
    async_optimize: async_optimize_cls = ...
    write_pdat: write_pdat_cls = ...
    confirm_overwrite: confirm_overwrite_cls = ...
    export: export_cls = ...
    import_: import__cls = ...
    parametric_project: parametric_project_cls = ...
    command_names = ...

    def auto_save(self, ):
        """
        'auto_save' child.
        """

    def define_macro(self, filename: str):
        """
        Save input to a named macro.
        
        Parameters
        ----------
            filename : str
                'filename' child.
        
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

