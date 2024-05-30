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

from .electrolyte_submodel_enabled import electrolyte_submodel_enabled as electrolyte_submodel_enabled_cls
from .vol_energy_enabled import vol_energy_enabled as vol_energy_enabled_cls
from .surf_energy_enabled import surf_energy_enabled as surf_energy_enabled_cls
from .knudsen_diff_enabled import knudsen_diff_enabled as knudsen_diff_enabled_cls
from .species_enabled import species_enabled as species_enabled_cls
from .electrolysis_mode_enabled import electrolysis_mode_enabled as electrolysis_mode_enabled_cls
from .co_echemistry_disabled import co_echemistry_disabled as co_echemistry_disabled_cls

class options(Group):
    fluent_name = ...
    child_names = ...
    electrolyte_submodel_enabled: electrolyte_submodel_enabled_cls = ...
    vol_energy_enabled: vol_energy_enabled_cls = ...
    surf_energy_enabled: surf_energy_enabled_cls = ...
    knudsen_diff_enabled: knudsen_diff_enabled_cls = ...
    species_enabled: species_enabled_cls = ...
    electrolysis_mode_enabled: electrolysis_mode_enabled_cls = ...
    co_echemistry_disabled: co_echemistry_disabled_cls = ...
