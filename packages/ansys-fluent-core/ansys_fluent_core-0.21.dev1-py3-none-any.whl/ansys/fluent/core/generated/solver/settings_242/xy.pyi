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

from .border_4 import border as border_cls
from .bottom_4 import bottom as bottom_cls
from .left_4 import left as left_cls
from .right_5 import right as right_cls
from .top_4 import top as top_cls
from .visible_6 import visible as visible_cls

class xy(Group):
    fluent_name = ...
    child_names = ...
    border: border_cls = ...
    bottom: bottom_cls = ...
    left: left_cls = ...
    right: right_cls = ...
    top: top_cls = ...
    visible: visible_cls = ...
