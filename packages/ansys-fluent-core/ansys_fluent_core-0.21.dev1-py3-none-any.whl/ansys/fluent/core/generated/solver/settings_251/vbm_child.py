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

from .name import name as name_cls
from .report_type import report_type as report_type_cls
from .vbm_rotor_name import vbm_rotor_name as vbm_rotor_name_cls
from .report_output_type_1 import report_output_type as report_output_type_cls
from .output_parameter_1 import output_parameter as output_parameter_cls
from .create_output_parameter import create_output_parameter as create_output_parameter_cls

class vbm_child(Group):
    """
    'child_object_type' of vbm.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'report_type', 'vbm_rotor_name', 'report_output_type',
         'output_parameter']

    command_names = \
        ['create_output_parameter']

    _child_classes = dict(
        name=name_cls,
        report_type=report_type_cls,
        vbm_rotor_name=vbm_rotor_name_cls,
        report_output_type=report_output_type_cls,
        output_parameter=output_parameter_cls,
        create_output_parameter=create_output_parameter_cls,
    )

