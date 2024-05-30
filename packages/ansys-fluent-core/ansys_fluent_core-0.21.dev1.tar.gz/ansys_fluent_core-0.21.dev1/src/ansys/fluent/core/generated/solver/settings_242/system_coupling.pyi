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

from .htc import htc as htc_cls
from .unsteady_statistics import unsteady_statistics as unsteady_statistics_cls
from .user_defined_coupling_variables_via_udm import user_defined_coupling_variables_via_udm as user_defined_coupling_variables_via_udm_cls
from .use_face_or_element_based_data_transfer import use_face_or_element_based_data_transfer as use_face_or_element_based_data_transfer_cls
from .activate_flow_boundary_coupling_model import activate_flow_boundary_coupling_model as activate_flow_boundary_coupling_model_cls
from .write_scp_file import write_scp_file as write_scp_file_cls
from .connect_parallel import connect_parallel as connect_parallel_cls
from .init_and_solve import init_and_solve as init_and_solve_cls
from .solve import solve as solve_cls

class system_coupling(Group):
    fluent_name = ...
    child_names = ...
    htc: htc_cls = ...
    unsteady_statistics: unsteady_statistics_cls = ...
    user_defined_coupling_variables_via_udm: user_defined_coupling_variables_via_udm_cls = ...
    use_face_or_element_based_data_transfer: use_face_or_element_based_data_transfer_cls = ...
    activate_flow_boundary_coupling_model: activate_flow_boundary_coupling_model_cls = ...
    command_names = ...

    def write_scp_file(self, file_name: str):
        """
        Write fluent input scp file for sc.
        
        Parameters
        ----------
            file_name : str
                'file_name' child.
        
        """

    def connect_parallel(self, schost: str, scport: int, scname: str):
        """
        System coupling connection status.
        
        Parameters
        ----------
            schost : str
                Sc solver host input.
            scport : int
                Sc solver port input.
            scname : str
                Sc solver name input.
        
        """

    def init_and_solve(self, ):
        """
        System-coupling-solve-init-command.
        """

    def solve(self, ):
        """
        System-coupling-solve-command.
        """

