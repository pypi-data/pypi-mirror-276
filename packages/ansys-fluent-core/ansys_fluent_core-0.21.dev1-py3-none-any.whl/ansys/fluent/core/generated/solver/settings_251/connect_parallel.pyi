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

from .schost import schost as schost_cls
from .scport import scport as scport_cls
from .scname import scname as scname_cls

class connect_parallel(Command):
    fluent_name = ...
    argument_names = ...
    schost: schost_cls = ...
    scport: scport_cls = ...
    scname: scname_cls = ...
