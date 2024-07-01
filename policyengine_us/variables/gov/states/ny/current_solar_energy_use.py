from policyengine_us.model_api import *



class ny_current_solar_energy_use(Variable):
    value_type = float
    entity = Household
    label = "Past year or projected year home energy use in annual kilowatt hours"
    unit = "kWh"
    definition_period = YEAR
    defined_for = StateCode.NY
    reference = ""