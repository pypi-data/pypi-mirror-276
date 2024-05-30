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

from .implicit_body_force import implicit_body_force as implicit_body_force_cls

class body_force_formulation(Group):
    fluent_name = ...
    child_names = ...
    implicit_body_force: implicit_body_force_cls = ...
