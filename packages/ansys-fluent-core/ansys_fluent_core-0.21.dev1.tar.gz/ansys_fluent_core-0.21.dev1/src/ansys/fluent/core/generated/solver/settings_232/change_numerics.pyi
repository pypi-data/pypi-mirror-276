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

from .use_sided_area_vector import use_sided_area_vector as use_sided_area_vector_cls
from .use_nci_sided_area_vectors import use_nci_sided_area_vectors as use_nci_sided_area_vectors_cls
from .recrete import recrete as recrete_cls

class change_numerics(Command):
    fluent_name = ...
    argument_names = ...
    use_sided_area_vector: use_sided_area_vector_cls = ...
    use_nci_sided_area_vectors: use_nci_sided_area_vectors_cls = ...
    recrete: recrete_cls = ...
