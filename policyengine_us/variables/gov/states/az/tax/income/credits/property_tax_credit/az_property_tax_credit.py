from policyengine_us.model_api import *


class az_property_tax_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = "Arizona Property Tax Credit"
    unit = USD
    definition_period = YEAR
    defined_for = "az_property_tax_credit_eligible"

    def formula(tax_unit, period, parameters):
        person = tax_unit.members
        p = parameters(period).gov.states.az.tax.income.property_tax_credits
        income = tax_unit("az_property_tax_credit_income", period)

        cohabitating = tax_unit("cohabitating_spouses", period)

        household_income_credit = select(
            [
                ~cohabitating,
                cohabitating,
            ],
            [
                p.amount.living_alone.calc(income),
                p.amount.cohabitating.calc(income),
            ],
        )

        property_tax = person("real_estate_taxes", period)
        rent = person("rent", period)
        payment_credit = property_tax + rent

        return min_(household_income_credit, payment_credit)
