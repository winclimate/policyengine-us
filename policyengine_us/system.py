from pathlib import Path
from policyengine_core.taxbenefitsystems import TaxBenefitSystem
from policyengine_us.entities import *
from policyengine_us.parameters.gov.irs.uprating import (
    set_irs_uprating_parameter,
)
from policyengine_core.simulations import (
    Simulation as CoreSimulation,
    Microsimulation as CoreMicrosimulation,
)
from policyengine_us.data import CPS
from policyengine_us.tools.dev.taxcalc.generate_taxcalc_variable import (
    add_taxcalc_variable_aliases,
)
from policyengine_us.variables.household.demographic.geographic.state.in_state import (
    create_50_state_variables,
)

COUNTRY_DIR = Path(__file__).parent


class CountryTaxBenefitSystem(TaxBenefitSystem):
    parameters_dir = COUNTRY_DIR / "parameters"
    variables_dir = COUNTRY_DIR / "variables"
    auto_carry_over_input_variables = True

    def __init__(self):
        # We initialize our tax and benefit system with the general constructor
        super().__init__(entities)

        self.add_variables(*create_50_state_variables())

        self.parameters = set_irs_uprating_parameter(self.parameters)

        add_taxcalc_variable_aliases(self)


class Simulation(CoreSimulation):
    default_tax_benefit_system = CountryTaxBenefitSystem
    default_role = "member"
    default_calculation_period = "2022"


class Microsimulation(CoreMicrosimulation):
    default_tax_benefit_system = CountryTaxBenefitSystem
    default_dataset = CPS
    default_dataset_year = 2021
    default_role = "member"
    default_calculation_period = "2022"
