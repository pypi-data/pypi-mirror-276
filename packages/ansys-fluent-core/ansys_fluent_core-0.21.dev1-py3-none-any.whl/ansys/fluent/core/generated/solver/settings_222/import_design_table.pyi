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

from .filepath import filepath as filepath_cls
from .delete_existing import delete_existing as delete_existing_cls

class import_design_table(Command):
    fluent_name = ...
    argument_names = ...
    filepath: filepath_cls = ...
    delete_existing: delete_existing_cls = ...
