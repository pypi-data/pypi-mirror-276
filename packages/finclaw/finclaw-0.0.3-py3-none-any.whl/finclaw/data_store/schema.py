import pyarrow as pa

# Stock symbol should be at directory level
OHCL = pa.schema([
    ("symbol", pa.string()),
    ("timestamp", pa.timestamp('s', tz="UTC")),
    ("open", pa.float64()),
    ("high", pa.float64()),
    ("close", pa.float64()),
    ("low", pa.float64()),
    ("volume", pa.int64())])

# TODO: Check what storage type to use for flaot

# market -> stock table that maps equity symbol to id
# market -> data -> id -> ohcl_resolution_dataset partitioned by date
# Add price validation for storage

# figi:https://www.openfigi.com/
# symbol -> ticker
# mic (Market Identifier): https://www.investopedia.com/terms/m/mic.asp#:~:text=A%20market%20identifier%20code%20(MIC)%20is%20used%20to%20specify%20stock,XNAS%20for%20the%20Nasdaq%20market.
# Name -> descriptions
STOCK_SYMBOL = pa.schema([
    ("ticker", pa.string()),
    ("figi", pa.string()),
    ("type", pa.string()),
    ("mic", pa.string()),
    ("description", pa.string()),
    ("currency_name", pa.string())
])

COMPANY_PROFILE = pa.schema([
    ("country", pa.string()),
    ("currency", pa.string()),
    ("exchange", pa.string()),
    ("sector", pa.string()),
    ("ipo", pa.timestamp("s", tz="UTC")),
    ("market_cap", pa.float64()),
    ("name", pa.string()),
    ("share_outstanding", pa.float64()),
    ("ticker", pa.string()),
])

NEWS = pa.schema([
    ("feed_url", pa.string()),
    ("title", pa.string()),
    ("url", pa.string()),
    ("description", pa.string()),
    ("timestamp", pa.timestamp('ms', tz="UTC")),
    ("website", pa.string())
])

SECTOR = pa.schema([
    ("symbol", pa.string()),
    ("sector", pa.string())
])

DIVIDEND = pa.schema([
    ("symbol", pa.string()),
    ("ex_date", pa.timestamp('s', tz="UTC")),
    ("payment_date", pa.timestamp('s', tz="UTC")),
    ("record_date", pa.timestamp('s', tz="UTC")),
    ("declared_date", pa.timestamp('s', tz="UTC")),
    ("amount", pa.float64()),
    ("currency", pa.string()),
    ("adjusted_amount", pa.float64())
])

INSIDER_TRANSACTION = pa.schema([
    ("symbol", pa.string()),
    ("transaction_date", pa.timestamp('s', tz="UTC")),
    ("transaction_type", pa.string()),
    ("shares_traded", pa.float64()),
    ("shares_owned", pa.float64()),
    ("price", pa.float64()),
    ("insider_name", pa.string()),
    ("filing_date", pa.timestamp('s', tz="UTC")),
])

INSTITUTIONAL_OWNERSHIP = pa.schema([
    ("symbol", pa.string()),
    ("report_date", pa.timestamp('s', tz="UTC")),
    ("organization", pa.string()),
    ("shares_owned", pa.float64()),
    ("value", pa.float64()),
    ("put_call", pa.string()),
    ("sole_voting", pa.float64()),
    ("shared_voting", pa.float64()),
    ("no_voting", pa.float64()),
    ("portfolio_percentage", pa.float64()),
    ("shares_traded", pa.float64()),
    ("cik", pa.string()),
    ("cusip", pa.string()),
])

FUND_OWNERSHIP = pa.schema([
    ("symbol", pa.string()),
    ("filling_date", pa.timestamp('s', tz="UTC")),
    ("fund_name", pa.string()),
    ("shares_held", pa.float64()),
    ("portfolio_percentage", pa.float64()),
    ("shares_traded", pa.float64()),
])

BALANCE_SHEET_FIELD_TYPES = {
    'inventory': pa.float32(),
    'cash_short_term_investments': pa.float32(),
    'tangible_book_value_per_share': pa.float32(),
    'goodwill': pa.float32(),
    'other_receivables': pa.float32(),
    'insurance_policy_liabilities': pa.float32(),
    'other_interest_bearing_liabilities': pa.float32(),
    'cash_due_from_banks': pa.float32(),
    'common_stock': pa.float32(),
    'shares_outstanding': pa.float32(),
    'intangibles_assets': pa.float32(),
    'minority_interest': pa.float32(),
    'total_debt': pa.float32(),
    'other_current_liabilities': pa.float32(),
    'accounts_receivables': pa.float32(),
    'other_long_term_assets': pa.float32(),
    'cash_equivalents': pa.float32(),
    'period': pa.timestamp('s', tz='UTC'),
    'additional_paid_in_capital': pa.float32(),
    'note_receivable_long_term': pa.float32(),
    'cash': pa.float32(),
    'total_deposits': pa.float32(),
    'long_term_debt': pa.float32(),
    'accounts_payable': pa.float32(),
    'current_portion_long_term_debt': pa.float32(),
    'accrued_liability': pa.float32(),
    'accumulated_depreciation': pa.float32(),
    'net_loans': pa.float32(),
    'long_term_investments': pa.float32(),
    'deferred_income_tax': pa.float32(),
    'net_debt': pa.float32(),
    'other_equity': pa.float32(),
    'other_liabilities': pa.float32(),
    'bank_investments': pa.float32(),
    'unrealized_profit_loss_security': pa.float32(),
    'customer_liability_acceptances': pa.float32(),
    'total_equity': pa.float32(),
    'retained_earnings': pa.float32(),
    'total_receivables': pa.float32(),
    'preferred_shares_outstanding': pa.float32(),
    'insurance_receivables': pa.float32(),
    'liabilities_shareholders_equity': pa.float32(),
    'total_assets': pa.float32(),
    'short_term_debt': pa.float32(),
    'current_liabilities': pa.float32(),
    'total_liabilities': pa.float32(),
    'symbol': pa.string(),
    'deferred_policy_acquisition_costs': pa.float32(),
    'current_assets': pa.float32(),
    'other_current_assets': pa.float32(),
    'short_term_investments': pa.float32(),
    'other_assets': pa.float32(),
    'treasury_stock': pa.float32(),
    'property_plant_equipment': pa.float32()
}

BALANCE_SHEET = pa.schema([pa.field(name, field_type) for name, field_type in BALANCE_SHEET_FIELD_TYPES.items()])

INCOME_STATEMENT = pa.schema([
    ('bank_non_interest_income', pa.float64()),
    ('research_development', pa.float64()),
    ('operations_maintenance', pa.float64()),
    ('revenue', pa.float64()),
    ('equity_earnings_affiliates', pa.float64()),
    ('sga_expense', pa.float64()),
    ('gross_income', pa.float64()),
    ('minority_interest', pa.float64()),
    ('purchased_fuel_power_gas', pa.float64()),
    ('interest_expense', pa.float64()),
    ('net_income', pa.float64()),
    ('period', pa.timestamp('s', tz='UTC')),
    ('net_interest_income', pa.float64()),
    ('bank_interest_income', pa.float64()),
    ('total_operating_expense', pa.float64()),
    ('other_revenue', pa.float64()),
    ('interest_income_expense', pa.float64()),
    ('benefits_claims_loss_adjustment', pa.float64()),
    ('diluted_e_p_s', pa.float64()),
    ('cost_of_goods_sold', pa.float64()),
    ('gain_loss_on_disposition_of_assets', pa.float64()),
    ('provision_for_income_taxes', pa.float64()),
    ('gross_premiums_earned', pa.float64()),
    ('other_operating_expenses_total', pa.float64()),
    ('non_recurring_items', pa.float64()),
    ('depreciation_amortization', pa.float64()),
    ('pretax_income', pa.float64()),
    ('total_other_income_expense_net', pa.float64()),
    ('ebit', pa.float64()),
    ('bank_non_interest_expense', pa.float64()),
    ('loan_loss_provision', pa.float64()),
    ('net_income_after_taxes', pa.float64()),
    ('diluted_average_shares_outstanding', pa.float64()),
    ('symbol', pa.string()),
    ('net_interest_inc_after_loan_loss_prov', pa.float64())
])

CASHFLOW_STATEMENT = pa.schema([
    ('cash_dividends_paid', pa.float64()),
    ('change_in_cash', pa.float64()),
    ('fcf', pa.float64()),
    ('net_investing_cash_flow', pa.float64()),
    ('cash_taxes_paid', pa.float64()),
    ('changes_in_working_capital', pa.float64()),
    ('net_cash_financing_activities', pa.float64()),
    ('depreciation_amortization', pa.float64()),
    ('deferred_taxes_investment_tax_credit', pa.float64()),
    ('capex', pa.float64()),
    ('other_investing_cash_flow_items_total', pa.float64()),
    ('period', pa.timestamp('s', tz='UTC')),
    ('issuance_reduction_capital_stock', pa.float64()),
    ('cash_interest_paid', pa.float64()),
    ('net_income_starting_line', pa.int64()),
    ('symbol', pa.string()),
    ('net_operating_cash_flow', pa.float64()),
    ('other_funds_financing_items', pa.float64()),
    ('foreign_exchange_effects', pa.float64()),
    ('other_funds_non_cash_items', pa.float64()),
    ('issuance_reduction_debt_net', pa.float64()),
    ('cash_net', pa.float64())
])

SPLIT = pa.schema([
    ('split_date', pa.timestamp('s', tz='UTC')),
    ('symbol', pa.string()),
    ('from_factor', pa.float64()),
    ('to_factor', pa.float64())
])

OWNER = pa.schema([
    ('shares_traded', pa.float64()),
    ('filing_date', pa.timestamp('s', tz='UTC')),
    ('name', pa.string()),
    ('shares_owned', pa.float64()),
    ('symbol', pa.string())
])

BALANCE_SHEET_V2 = pa.schema([
    ('date', pa.timestamp('ns')),
    ('symbol', pa.string()),
    ('reported_currency', pa.string()),
    ('cik', pa.string()),
    ('filling_date', pa.timestamp('ns')),
    ('accepted_date', pa.timestamp('ns')),
    ('calendar_year', pa.timestamp('ns')),
    ('period', pa.string()),
    ('cash_and_cash_equivalents', pa.float64()),
    ('short_term_investments', pa.float64()),
    ('cash_and_short_term_investments', pa.float64()),
    ('net_receivables', pa.float64()),
    ('inventory', pa.float64()),
    ('other_current_assets', pa.float64()),
    ('total_current_assets', pa.float64()),
    ('property_plant_equipment_net', pa.float64()),
    ('goodwill', pa.float64()),
    ('intangible_assets', pa.float64()),
    ('goodwill_and_intangible_assets', pa.float64()),
    ('long_term_investments', pa.float64()),
    ('tax_assets', pa.float64()),
    ('other_non_current_assets', pa.float64()),
    ('total_non_current_assets', pa.float64()),
    ('other_assets', pa.float64()),
    ('total_assets', pa.float64()),
    ('account_payables', pa.float64()),
    ('short_term_debt', pa.float64()),
    ('tax_payables', pa.float64()),
    ('deferred_revenue', pa.float64()),
    ('other_current_liabilities', pa.float64()),
    ('total_current_liabilities', pa.float64()),
    ('long_term_debt', pa.float64()),
    ('deferred_revenue_non_current', pa.float64()),
    ('deferred_tax_liabilities_non_current', pa.float64()),
    ('other_non_current_liabilities', pa.float64()),
    ('total_non_current_liabilities', pa.float64()),
    ('other_liabilities', pa.float64()),
    ('capital_lease_obligations', pa.float64()),
    ('total_liabilities', pa.float64()),
    ('preferred_stock', pa.float64()),
    ('common_stock', pa.float64()),
    ('retained_earnings', pa.float64()),
    ('accumulated_other_comprehensive_income_loss', pa.float64()),
    ('othertotal_stockholders_equity', pa.float64()),
    ('total_stockholders_equity', pa.float64()),
    ('total_equity', pa.float64()),
    ('total_liabilities_and_stockholders_equity', pa.float64()),
    ('minority_interest', pa.float64()),
    ('total_liabilities_and_total_equity', pa.float64()),
    ('total_investments', pa.float64()),
    ('total_debt', pa.float64()),
    ('net_debt', pa.float64()),
    ('link', pa.string()),
    ('final_link', pa.string())
])

INCOME_STATEMENT_V2 = pa.schema([
    ('date', pa.timestamp('ns')),
    ('symbol', pa.string()),
    ('reported_currency', pa.string()),
    ('cik', pa.string()),
    ('filling_date', pa.timestamp('ns')),
    ('accepted_date', pa.timestamp('ns')),
    ('calendar_year', pa.timestamp('ns')),
    ('period', pa.string()),
    ('revenue', pa.float64()),
    ('cost_of_revenue', pa.float64()),
    ('gross_profit', pa.float64()),
    ('gross_profit_ratio', pa.float64()),
    ('research_and_development_expenses', pa.float64()),
    ('general_and_administrative_expenses', pa.float64()),
    ('selling_and_marketing_expenses', pa.float64()),
    ('selling_general_and_administrative_expenses', pa.float64()),
    ('other_expenses', pa.float64()),
    ('operating_expenses', pa.float64()),
    ('cost_and_expenses', pa.float64()),
    ('interest_income', pa.float64()),
    ('interest_expense', pa.float64()),
    ('depreciation_and_amortization', pa.float64()),
    ('ebitda', pa.float64()),
    ('ebitda_ratio', pa.float64()),
    ('operating_income', pa.float64()),
    ('operating_income_ratio', pa.float64()),
    ('total_other_income_expenses_net', pa.float64()),
    ('income_before_tax', pa.float64()),
    ('income_before_tax_ratio', pa.float64()),
    ('income_tax_expense', pa.float64()),
    ('net_income', pa.float64()),
    ('net_income_ratio', pa.float64()),
    ('eps', pa.float64()),
    ('eps_diluted', pa.float64()),
    ('weighted_average_shs_out', pa.float64()),
    ('weighted_average_shs_out_dil', pa.float64()),
    ('link', pa.string()),
    ('final_link', pa.string())
])

CASHFLOW_STATEMENT_V2 = pa.schema([
    ('date', pa.timestamp('ns')),
    ('symbol', pa.string()),
    ('reported_currency', pa.string()),
    ('cik', pa.string()),
    ('filling_date', pa.timestamp('ns')),
    ('accepted_date', pa.timestamp('ns')),
    ('calendar_year', pa.timestamp('ns')),
    ('period', pa.string()),
    ('net_income', pa.float64()),
    ('depreciation_and_amortization', pa.float64()),
    ('deferred_income_tax', pa.float64()),
    ('stock_based_compensation', pa.float64()),
    ('change_in_working_capital', pa.float64()),
    ('accounts_receivables', pa.float64()),
    ('inventory', pa.float64()),
    ('accounts_payables', pa.float64()),
    ('other_working_capital', pa.float64()),
    ('other_non_cash_items', pa.float64()),
    ('net_cash_provided_by_operating_activities', pa.float64()),
    ('investments_in_property_plant_and_equipment', pa.float64()),
    ('acquisitions_net', pa.float64()),
    ('purchases_of_investments', pa.float64()),
    ('sales_maturities_of_investments', pa.float64()),
    ('other_investing_activities', pa.float64()),
    ('net_cash_used_for_investing_activities', pa.float64()),
    ('debt_repayment', pa.float64()),
    ('common_stock_issued', pa.float64()),
    ('common_stock_repurchased', pa.float64()),
    ('dividends_paid', pa.float64()),
    ('other_financing_activities', pa.float64()),
    ('net_cash_used_provided_by_financing_activities', pa.float64()),
    ('effect_of_forex_changes_on_cash', pa.float64()),
    ('net_change_in_cash', pa.float64()),
    ('cash_at_end_of_period', pa.float64()),
    ('cash_at_beginning_of_period', pa.float64()),
    ('operating_cash_flow', pa.float64()),
    ('capital_expenditure', pa.float64()),
    ('free_cash_flow', pa.float64()),
    ('link', pa.string()),
    ('final_link', pa.string())
])
