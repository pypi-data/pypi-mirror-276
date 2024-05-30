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

from .option_2 import option as option_cls
from .cone_type import cone_type as cone_type_cls
from .inject_as_film import inject_as_film as inject_as_film_cls

class injection_type(Group):
    fluent_name = ...
    child_names = ...
    option: option_cls = ...
    cone_type: cone_type_cls = ...
    inject_as_film: inject_as_film_cls = ...
