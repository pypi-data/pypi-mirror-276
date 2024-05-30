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

from .name_8 import name as name_cls
from .home_options import home_options as home_options_cls
from .transparency_options import transparency_options as transparency_options_cls
from .isovalue_options import isovalue_options as isovalue_options_cls
from .clip_box_options import clip_box_options as clip_box_options_cls
from .clip_sphere_options import clip_sphere_options as clip_sphere_options_cls
from .compute_node_count import compute_node_count as compute_node_count_cls
from .display_3 import display as display_cls

class volumes_child(Group):
    fluent_name = ...
    child_names = ...
    name: name_cls = ...
    home_options: home_options_cls = ...
    transparency_options: transparency_options_cls = ...
    isovalue_options: isovalue_options_cls = ...
    clip_box_options: clip_box_options_cls = ...
    clip_sphere_options: clip_sphere_options_cls = ...
    compute_node_count: compute_node_count_cls = ...
    command_names = ...

    def display(self, ):
        """
        'display' command.
        """

