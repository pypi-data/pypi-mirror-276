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

from .particle_mixture_child import particle_mixture_child


class particle_mixture(NamedObject[particle_mixture_child], _CreatableNamedObjectMixin[particle_mixture_child]):
    """
    'particle_mixture' child.
    """

    fluent_name = "particle-mixture"

    child_object_type: particle_mixture_child = particle_mixture_child
    """
    child_object_type of particle_mixture.
    """
