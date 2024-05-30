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

from .name import name as name_cls
from .bndry_threads import bndry_threads as bndry_threads_cls
from .surfaces import surfaces as surfaces_cls
from .structural_analysis import structural_analysis as structural_analysis_cls
from .write_loads import write_loads as write_loads_cls
from .loads import loads as loads_cls
from .cell_func_domain_export import cell_func_domain_export as cell_func_domain_export_cls

class nastran(Command):
    fluent_name = ...
    argument_names = ...
    name: name_cls = ...
    bndry_threads: bndry_threads_cls = ...
    surfaces: surfaces_cls = ...
    structural_analysis: structural_analysis_cls = ...
    write_loads: write_loads_cls = ...
    loads: loads_cls = ...
    cell_func_domain_export: cell_func_domain_export_cls = ...
