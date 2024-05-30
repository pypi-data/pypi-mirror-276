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

from .name_1 import name as name_cls
from .animate_on import animate_on as animate_on_cls
from .frequency_1 import frequency as frequency_cls
from .flow_time_frequency import flow_time_frequency as flow_time_frequency_cls
from .frequency_of import frequency_of as frequency_of_cls
from .storage_type import storage_type as storage_type_cls
from .storage_dir import storage_dir as storage_dir_cls
from .window_id import window_id as window_id_cls
from .view import view as view_cls
from .use_raytracing import use_raytracing as use_raytracing_cls
from .display_3 import display as display_cls

class solution_animations_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    animate_on: animate_on_cls = ...
    frequency: frequency_cls = ...
    flow_time_frequency: flow_time_frequency_cls = ...
    frequency_of: frequency_of_cls = ...
    storage_type: storage_type_cls = ...
    storage_dir: storage_dir_cls = ...
    window_id: window_id_cls = ...
    view: view_cls = ...
    use_raytracing: use_raytracing_cls = ...
    command_names = ...

    def display(self, ):
        """
        'display' command.
        """

