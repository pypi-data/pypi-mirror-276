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

from .face_pressure_options import face_pressure_options as face_pressure_options_cls

class face_pressure_controls(Group):
    fluent_name = ...
    child_names = ...
    face_pressure_options: face_pressure_options_cls = ...
