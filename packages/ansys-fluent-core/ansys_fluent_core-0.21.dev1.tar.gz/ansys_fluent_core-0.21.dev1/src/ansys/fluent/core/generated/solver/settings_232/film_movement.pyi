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

from .condensing_film import condensing_film as condensing_film_cls
from .all_film import all_film as all_film_cls

class film_movement(Group):
    fluent_name = ...
    child_names = ...
    condensing_film: condensing_film_cls = ...
    all_film: all_film_cls = ...
