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

from .turbulence_design_variables import turbulence_design_variables as turbulence_design_variables_cls

class initialize(Command):
    """
    Initialize gradient-based optimizer.
    
    Parameters
    ----------
        turbulence_design_variables : bool
            Initialize the turbulence design variables in the design region?.
    
    """

    fluent_name = "initialize"

    argument_names = \
        ['turbulence_design_variables']

    _child_classes = dict(
        turbulence_design_variables=turbulence_design_variables_cls,
    )

