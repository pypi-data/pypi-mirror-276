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

from .mesh_1 import mesh as mesh_cls
from .surface_1 import surface as surface_cls
from .volume import volume as volume_cls
from .force import force as force_cls
from .lift import lift as lift_cls
from .drag import drag as drag_cls
from .moment import moment as moment_cls
from .time_1 import time as time_cls
from .flux_1 import flux as flux_cls
from .vbm import vbm as vbm_cls
from .injection_1 import injection as injection_cls
from .user_defined_6 import user_defined as user_defined_cls
from .aeromechanics import aeromechanics as aeromechanics_cls
from .icing_3 import icing as icing_cls
from .expression_1 import expression as expression_cls
from .single_valued_expression import single_valued_expression as single_valued_expression_cls
from .custom import custom as custom_cls
from .compute_2 import compute as compute_cls
from .copy_2 import copy as copy_cls

class report_definitions(Group, _ChildNamedObjectAccessorMixin):
    fluent_name = ...
    child_names = ...
    mesh: mesh_cls = ...
    surface: surface_cls = ...
    volume: volume_cls = ...
    force: force_cls = ...
    lift: lift_cls = ...
    drag: drag_cls = ...
    moment: moment_cls = ...
    time: time_cls = ...
    flux: flux_cls = ...
    vbm: vbm_cls = ...
    injection: injection_cls = ...
    user_defined: user_defined_cls = ...
    aeromechanics: aeromechanics_cls = ...
    icing: icing_cls = ...
    expression: expression_cls = ...
    single_valued_expression: single_valued_expression_cls = ...
    custom: custom_cls = ...
    command_names = ...

    def compute(self, report_defs: List[str]):
        """
        Allows you to compute and view the net value.
        
        Parameters
        ----------
            report_defs : typing.List[str]
                Compute the net value of the selected report definition.
        
        """

    def copy(self, copy_from: str, copy_to: str):
        """
        Create a copy of a report definition.
        
        Parameters
        ----------
            copy_from : str
                Select the report definition to copy.
            copy_to : str
                Write the new name for the copied report definition.
        
        """

