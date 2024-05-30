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

from .ecad_name import ecad_name as ecad_name_cls
from .choice import choice as choice_cls
from .rows import rows as rows_cls
from .columns import columns as columns_cls
from .ref_frame import ref_frame as ref_frame_cls
from .pwr_names import pwr_names as pwr_names_cls

class pcb_zone_info(Group):
    fluent_name = ...
    child_names = ...
    ecad_name: ecad_name_cls = ...
    choice: choice_cls = ...
    rows: rows_cls = ...
    columns: columns_cls = ...
    ref_frame: ref_frame_cls = ...
    pwr_names: pwr_names_cls = ...
