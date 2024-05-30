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

from .only_list_case_boundaries import only_list_case_boundaries as only_list_case_boundaries_cls
from .use_inherent_material_color import use_inherent_material_color as use_inherent_material_color_cls
from .type_name import type_name as type_name_cls
from .reset_2 import reset as reset_cls

class by_type(Group):
    fluent_name = ...
    child_names = ...
    only_list_case_boundaries: only_list_case_boundaries_cls = ...
    use_inherent_material_color: use_inherent_material_color_cls = ...
    type_name: type_name_cls = ...
    command_names = ...

    def reset(self, ):
        """
        To reset colors and/or materials to the defaults.
        """

