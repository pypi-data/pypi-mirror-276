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

from .name_8 import name as name_cls
from .animate_on import animate_on as animate_on_cls
from .frequency_of_1 import frequency_of as frequency_of_cls
from .frequency_3 import frequency as frequency_cls
from .flow_time_frequency import flow_time_frequency as flow_time_frequency_cls
from .last_flow_time import last_flow_time as last_flow_time_cls
from .append_filename_with import append_filename_with as append_filename_with_cls
from .storage_type import storage_type as storage_type_cls
from .storage_dir import storage_dir as storage_dir_cls
from .window_id import window_id as window_id_cls
from .view import view as view_cls
from .use_raytracing import use_raytracing as use_raytracing_cls
from .append_filename import append_filename as append_filename_cls
from .appended_flowtime_precision import appended_flowtime_precision as appended_flowtime_precision_cls
from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .display_2 import display as display_cls
from .copy_4 import copy as copy_cls
from .add_to_graphics import add_to_graphics as add_to_graphics_cls
from .clear_history import clear_history as clear_history_cls
from .solution_animations_child import solution_animations_child


class solution_animations(NamedObject[solution_animations_child], _CreatableNamedObjectMixin[solution_animations_child]):
    """
    'solution_animations' child.
    """

    fluent_name = "solution-animations"

    child_names = \
        ['name', 'animate_on', 'frequency_of', 'frequency',
         'flow_time_frequency', 'last_flow_time', 'append_filename_with',
         'storage_type', 'storage_dir', 'window_id', 'view', 'use_raytracing',
         'append_filename', 'appended_flowtime_precision']

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy',
         'display', 'copy', 'add_to_graphics', 'clear_history']

    _child_classes = dict(
        name=name_cls,
        animate_on=animate_on_cls,
        frequency_of=frequency_of_cls,
        frequency=frequency_cls,
        flow_time_frequency=flow_time_frequency_cls,
        last_flow_time=last_flow_time_cls,
        append_filename_with=append_filename_with_cls,
        storage_type=storage_type_cls,
        storage_dir=storage_dir_cls,
        window_id=window_id_cls,
        view=view_cls,
        use_raytracing=use_raytracing_cls,
        append_filename=append_filename_cls,
        appended_flowtime_precision=appended_flowtime_precision_cls,
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        display=display_cls,
        copy=copy_cls,
        add_to_graphics=add_to_graphics_cls,
        clear_history=clear_history_cls,
    )

    child_object_type: solution_animations_child = solution_animations_child
    """
    child_object_type of solution_animations.
    """
