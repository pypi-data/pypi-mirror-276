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

from .design_region import design_region as design_region_cls
from .design_variables import design_variables as design_variables_cls
from .model_4 import model as model_cls

class turbulence_model_design_tool(Group):
    fluent_name = ...
    child_names = ...
    design_region: design_region_cls = ...
    design_variables: design_variables_cls = ...
    model: model_cls = ...
