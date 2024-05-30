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

from .from__1 import from_ as from__cls
from .to_1 import to as to_cls
from .verbosity_3 import verbosity as verbosity_cls

class copy(Command):
    fluent_name = ...
    argument_names = ...
    from_: from__cls = ...
    to: to_cls = ...
    verbosity: verbosity_cls = ...
