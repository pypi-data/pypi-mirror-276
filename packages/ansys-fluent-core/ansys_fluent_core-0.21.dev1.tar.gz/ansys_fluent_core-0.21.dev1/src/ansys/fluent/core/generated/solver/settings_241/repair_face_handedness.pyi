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

from .repair_1 import repair as repair_cls
from .disable_repair import disable_repair as disable_repair_cls

class repair_face_handedness(Command):
    fluent_name = ...
    argument_names = ...
    repair: repair_cls = ...
    disable_repair: disable_repair_cls = ...
