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

from .module_case_file import module_case_file as module_case_file_cls
from .cold_plate_file import cold_plate_file as cold_plate_file_cls
from .nci_face_list import nci_face_list as nci_face_list_cls
from .translation_rotation_matrix import translation_rotation_matrix as translation_rotation_matrix_cls
from .read_location_file import read_location_file as read_location_file_cls
from .write_location_file import write_location_file as write_location_file_cls
from .construct_battery_pack import construct_battery_pack as construct_battery_pack_cls
from .nci_pair_creation import nci_pair_creation as nci_pair_creation_cls

class pack_builder(Group):
    fluent_name = ...
    child_names = ...
    module_case_file: module_case_file_cls = ...
    cold_plate_file: cold_plate_file_cls = ...
    nci_face_list: nci_face_list_cls = ...
    translation_rotation_matrix: translation_rotation_matrix_cls = ...
    command_names = ...

    def read_location_file(self, file_name_1: str):
        """
        Command object to read location file in the pack builder.
        
        Parameters
        ----------
            file_name_1 : str
                Module Location file name with its full path.
        
        """

    def write_location_file(self, file_name: str):
        """
        Command object to write location file in the pack builder.
        
        Parameters
        ----------
            file_name : str
                Write location information into a file in the pack builder.
        
        """

    def construct_battery_pack(self, ):
        """
        Construct battery pack.
        """

    def nci_pair_creation(self, ):
        """
        Non-conformal Interface Matching in the pack builder.
        """

