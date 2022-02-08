import pandas as pd
from openfisca_us.model_api import *


class SNAPRegion(Enum):
    CONTIGUOUS_US = "Contiguous US"
    AK_URBAN = "Alaska (urban)"
    AK_RURAL_1 = "Alaska (rural 1)"
    AK_RURAL_2 = "Alaska (rural 2)"
    GU = "Guam"
    HI = "Hawaii"
    VI = "Virgin Islands"


class snap_region(Variable):
    value_type = Enum
    possible_values = SNAPRegion
    default_value = SNAPRegion.CONTIGUOUS_US
    entity = Household
    definition_period = YEAR
    label = "SNAP region"

    def formula(household, period):
        state_group = household("state_group", period)
        state_groups = state_group.possible_values
        mapped_values = (
            pd.Series(state_group.decode_to_str())
            .map(
                {
                    state_groups.AK: SNAPRegion.AK_URBAN,
                    **{
                        key: value
                        for key, value in SNAPRegion._member_map_.items()
                    },
                }
            )
            .values
        )
        return SNAPRegion.encode(mapped_values)


class snap_region_str(Variable):
    value_type = str
    entity = Household
    label = "SNAP region"
    definition_period = YEAR

    def formula(household, period):
        return [
            enum.value for enum in household("snap_region", period).decode()
        ]
