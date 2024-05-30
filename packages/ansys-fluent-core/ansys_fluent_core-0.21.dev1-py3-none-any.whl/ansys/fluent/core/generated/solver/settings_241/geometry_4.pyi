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

from .parts import parts as parts_cls
from .list_topology import list_topology as list_topology_cls

class geometry(Group):
    fluent_name = ...
    child_names = ...
    parts: parts_cls = ...
    command_names = ...

    def list_topology(self, ):
        """
        'list_topology' command.
        """

