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

from .ninjections import ninjections as ninjections_cls
from .urf import urf as urf_cls
from .injection import injection as injection_cls

class model_setup(Group):
    fluent_name = ...
    child_names = ...
    ninjections: ninjections_cls = ...
    urf: urf_cls = ...
    injection: injection_cls = ...
