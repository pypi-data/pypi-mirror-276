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

from .periodic_zone_name import periodic_zone_name as periodic_zone_name_cls
from .slit_periodic import slit_periodic as slit_periodic_cls

class slit_periodic(Command):
    fluent_name = ...
    argument_names = ...
    periodic_zone_name: periodic_zone_name_cls = ...
    slit_periodic: slit_periodic_cls = ...
