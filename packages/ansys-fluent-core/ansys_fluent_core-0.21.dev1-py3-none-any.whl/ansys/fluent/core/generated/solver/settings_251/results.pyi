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

from .custom_vectors import custom_vectors as custom_vectors_cls
from .surfaces_9 import surfaces as surfaces_cls
from .graphics import graphics as graphics_cls
from .plot_11 import plot as plot_cls
from .scene import scene as scene_cls
from .animations import animations as animations_cls
from .report_2 import report as report_cls

class results(Group):
    fluent_name = ...
    child_names = ...
    custom_vectors: custom_vectors_cls = ...
    surfaces: surfaces_cls = ...
    graphics: graphics_cls = ...
    plot: plot_cls = ...
    scene: scene_cls = ...
    animations: animations_cls = ...
    report: report_cls = ...
