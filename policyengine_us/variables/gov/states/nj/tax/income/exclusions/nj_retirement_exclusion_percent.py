from policyengine_us.model_api import *


class nj_retirement_exclusion_percent(Variable):
    value_type = float
    entity = TaxUnit
    label = "New Jersey retirement exclusion percent based on total income"
    unit = USD
    definition_period = YEAR
    reference = (
        "https://www.state.nj.us/treasury/taxation/pdf/current/1040i.pdf#page=21",
        "https://law.justia.com/codes/new-jersey/2022/title-54a/section-54a-6-10/",
    )
    defined_for = StateCode.NJ

    def formula(tax_unit, period, parameters):
        total_income = tax_unit("nj_total_income", period)
        filing_status = tax_unit("filing_status", period)
        status = filing_status.possible_values
        p = parameters(period).gov.states.nj.tax.income.exclusions.retirement
        return select(
            [
                filing_status == status.SINGLE,
                filing_status == status.JOINT,
                filing_status == status.HEAD_OF_HOUSEHOLD,
                filing_status == status.WIDOW,
                filing_status == status.SEPARATE,
            ],
            [
                p.percentage.single.calc(total_income),
                p.percentage.joint.calc(total_income),
                p.percentage.head_of_household.calc(total_income),
                p.percentage.widow.calc(total_income),
                p.percentage.separate.calc(total_income),
            ],
        )
