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

from .zonename import zonename as zonename_cls
from .newname import newname as newname_cls

class set_zone_name(Command):
    fluent_name = ...
    argument_names = ...
    zonename: zonename_cls = ...
    newname: newname_cls = ...
