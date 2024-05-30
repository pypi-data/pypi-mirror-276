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

from .use_enhancement import use_enhancement as use_enhancement_cls
from .aspect_ratio_1 import aspect_ratio as aspect_ratio_cls

class stretched_mesh_enhancement(Group):
    fluent_name = ...
    child_names = ...
    use_enhancement: use_enhancement_cls = ...
    aspect_ratio: aspect_ratio_cls = ...
