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
from .read_location_file import read_location_file as read_location_file_cls
from .nci_face_list import nci_face_list as nci_face_list_cls
from .construct_battery_pack import construct_battery_pack as construct_battery_pack_cls
from .nci_pair_creation import nci_pair_creation as nci_pair_creation_cls

class pack_builder(Group):
    fluent_name = ...
    child_names = ...
    module_case_file: module_case_file_cls = ...
    cold_plate_file: cold_plate_file_cls = ...
    read_location_file: read_location_file_cls = ...
    nci_face_list: nci_face_list_cls = ...
    command_names = ...

    def construct_battery_pack(self, ):
        """
        Construct battery pack.
        """

    def nci_pair_creation(self, ):
        """
        Non-conformal Interface Matching.
        """

