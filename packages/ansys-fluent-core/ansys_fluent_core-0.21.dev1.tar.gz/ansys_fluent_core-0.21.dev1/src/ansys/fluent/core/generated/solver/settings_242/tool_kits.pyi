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

from .standalone_echem_model import standalone_echem_model as standalone_echem_model_cls
from .parameter_estimation_tool import parameter_estimation_tool as parameter_estimation_tool_cls
from .rom_tool_kit import rom_tool_kit as rom_tool_kit_cls
from .pack_builder import pack_builder as pack_builder_cls

class tool_kits(Group):
    fluent_name = ...
    child_names = ...
    standalone_echem_model: standalone_echem_model_cls = ...
    parameter_estimation_tool: parameter_estimation_tool_cls = ...
    rom_tool_kit: rom_tool_kit_cls = ...
    pack_builder: pack_builder_cls = ...
