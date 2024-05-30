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

from .repair_angle import repair_angle as repair_angle_cls
from .periodic_input import periodic_input as periodic_input_cls
from .angle_input import angle_input as angle_input_cls
from .repair_periodic import repair_periodic as repair_periodic_cls

class repair_periodic(Command):
    fluent_name = ...
    argument_names = ...
    repair_angle: repair_angle_cls = ...
    periodic_input: periodic_input_cls = ...
    angle_input: angle_input_cls = ...
    repair_periodic: repair_periodic_cls = ...
