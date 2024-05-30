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

from .initial_dod import initial_dod as initial_dod_cls
from .ref_capacity import ref_capacity as ref_capacity_cls
from .data_type import data_type as data_type_cls
from .poly_u_function import poly_u_function as poly_u_function_cls
from .poly_y_function import poly_y_function as poly_y_function_cls
from .poly_t_dependence import poly_t_dependence as poly_t_dependence_cls
from .u_table import u_table as u_table_cls
from .y_table import y_table as y_table_cls
from .internal_resistance_table import internal_resistance_table as internal_resistance_table_cls
from .limit_current_enabled import limit_current_enabled as limit_current_enabled_cls
from .provide_utable_enabled import provide_utable_enabled as provide_utable_enabled_cls
from .limit_current_table import limit_current_table as limit_current_table_cls
from .monitor_names import monitor_names as monitor_names_cls
from .raw_data import raw_data as raw_data_cls

class ntgk_model_settings(Group):
    fluent_name = ...
    child_names = ...
    initial_dod: initial_dod_cls = ...
    ref_capacity: ref_capacity_cls = ...
    data_type: data_type_cls = ...
    poly_u_function: poly_u_function_cls = ...
    poly_y_function: poly_y_function_cls = ...
    poly_t_dependence: poly_t_dependence_cls = ...
    u_table: u_table_cls = ...
    y_table: y_table_cls = ...
    internal_resistance_table: internal_resistance_table_cls = ...
    limit_current_enabled: limit_current_enabled_cls = ...
    provide_utable_enabled: provide_utable_enabled_cls = ...
    limit_current_table: limit_current_table_cls = ...
    monitor_names: monitor_names_cls = ...
    command_names = ...

    def raw_data(self, import_files_enabled: bool, number_of_files: int, files: List[str], capacify_fade_enabled: bool):
        """
        Specify U and Y parameters using raw data.
        
        Parameters
        ----------
            import_files_enabled : bool
                Import raw data in the NTGK model.
            number_of_files : int
                Total number of discharging files.
            files : typing.List[str]
                Discharging file names in the NTGK model.
            capacify_fade_enabled : bool
                Enable capacity fade model in the NTGK model.
        
        """

