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

from .enabled_31 import enabled as enabled_cls
from .model_parameters import model_parameters as model_parameters_cls
from .electrochemistry import electrochemistry as electrochemistry_cls
from .electrolyte_porous import electrolyte_porous as electrolyte_porous_cls
from .electric_field import electric_field as electric_field_cls
from .customized_udf import customized_udf as customized_udf_cls

class sofc(Group):
    fluent_name = ...
    child_names = ...
    enabled: enabled_cls = ...
    model_parameters: model_parameters_cls = ...
    electrochemistry: electrochemistry_cls = ...
    electrolyte_porous: electrolyte_porous_cls = ...
    electric_field: electric_field_cls = ...
    customized_udf: customized_udf_cls = ...
