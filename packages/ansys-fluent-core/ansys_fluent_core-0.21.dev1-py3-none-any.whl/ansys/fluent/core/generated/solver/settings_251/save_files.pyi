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

from .frequency_7 import frequency as frequency_cls
from .maximum_5 import maximum as maximum_cls

class save_files(Group):
    fluent_name = ...
    child_names = ...
    frequency: frequency_cls = ...
    maximum: maximum_cls = ...
