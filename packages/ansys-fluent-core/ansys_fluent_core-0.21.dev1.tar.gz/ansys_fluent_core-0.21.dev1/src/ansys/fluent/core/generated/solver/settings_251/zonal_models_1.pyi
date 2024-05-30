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

from .zonal_models import zonal_models as zonal_models_cls
from .zonal_flow import zonal_flow as zonal_flow_cls
from .zonal_flow_spec import zonal_flow_spec as zonal_flow_spec_cls

class zonal_models(Group):
    fluent_name = ...
    child_names = ...
    zonal_models: zonal_models_cls = ...
    zonal_flow: zonal_flow_cls = ...
    zonal_flow_spec: zonal_flow_spec_cls = ...
