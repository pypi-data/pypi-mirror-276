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

from .sensitivity_orientation import sensitivity_orientation as sensitivity_orientation_cls
from .surface_shape_sensitivity import surface_shape_sensitivity as surface_shape_sensitivity_cls
from .reset_default import reset_default as reset_default_cls

class postprocess_options(Group):
    fluent_name = ...
    child_names = ...
    sensitivity_orientation: sensitivity_orientation_cls = ...
    surface_shape_sensitivity: surface_shape_sensitivity_cls = ...
    command_names = ...

    def reset_default(self, ):
        """
        Set postprocess options to default values.
        """

