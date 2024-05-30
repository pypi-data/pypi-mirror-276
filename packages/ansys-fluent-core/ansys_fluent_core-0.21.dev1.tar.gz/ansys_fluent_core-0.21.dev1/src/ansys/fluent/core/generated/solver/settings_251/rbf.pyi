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

from .freeform_motions_1 import freeform_motions as freeform_motions_cls
from .constraint_settings import constraint_settings as constraint_settings_cls

class rbf(Group):
    fluent_name = ...
    child_names = ...
    freeform_motions: freeform_motions_cls = ...
    constraint_settings: constraint_settings_cls = ...
