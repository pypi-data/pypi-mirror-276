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

from .filename import filename as filename_cls
from .unit import unit as unit_cls

class read(Command):
    """
    Read surface meshes.
    
    Parameters
    ----------
        filename : str
            'filename' child.
        unit : str
            'unit' child.
    
    """

    fluent_name = "read"

    argument_names = \
        ['filename', 'unit']

    _child_classes = dict(
        filename=filename_cls,
        unit=unit_cls,
    )

