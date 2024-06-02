# Use pydantic model for checking type
# https://finnhub.io/docs/api/stock-candles
from typing import List, Optional, Dict

import pandas as pd

from finclaw.data_store.schema import OHCL, COMPANY_PROFILE, DIVIDEND, INSIDER_TRANSACTION, INSTITUTIONAL_OWNERSHIP, \
    FUND_OWNERSHIP, BALANCE_SHEET, INCOME_STATEMENT, CASHFLOW_STATEMENT, SPLIT, OWNER
from finclaw.config import logger
import pyarrow as pa

from finclaw.vendor.finnhub.finnhub_to_table import FINNHUB_CANDLES_TO_OHCL_TABLE_MAP, \
    FINNHUB_COMPANY_NAME_TO_COMPANY_DESCRIPTION, FINNHUB_DIVIDEND_TO_DIVIDEND_TABLE_MAP, \
    FINNHUB_INSIDER_TO_INSIDER_TABLE_MAP, FINNHUB_OWNER_TO_INSTITUTIONAL_OWNERSHIP_TABLE_MAP, \
    FINNHUB_FUND_OWNERSHIP_TO_FUND_OWNERSHIP_TABLE_MAP, FINNHUB_BALANCE_SHEET_TO_BALANCE_SHEET_TABLE, \
    FINNHUB_INCOME_STATEMENT_TO_INCOME_STATEMENT_TABLE, FINNHUB_CASHFLOW_STATEMENT_TO_CASHFLOW_STATEMENT_TABLE, \
    FINNHUB_SPLIT_TO_SPLIT_TABLE, FINNHUB_OWNER_TO_OWNER_TABLE


# NOTE: I should use frozen set for this since it takes less memory in python
#       - It should also provide mapping to pyspark when saving
#       - I should add a test to it as well
#       - The returned data is in column format so I might need to cast it to pandas and then to
#       - To pyarrow and save, maybe there's a way to get it into pyarrow right away


def to_fund_ownership_table_column_names(data: dict) -> dict:
    return {new_column_name: data[column_name] for column_name, new_column_name in
            FINNHUB_FUND_OWNERSHIP_TO_FUND_OWNERSHIP_TABLE_MAP.items()}


def to_fund_ownership_table(data: dict) -> pa.Table:
    result = []

    symbol = data["symbol"]
    processed_data = []
    for d in data["ownership"]:
        record = {"symbol": symbol}
        record |= d
        processed_data.append(record)

    for fund_ownership_record in processed_data:
        standard_table = to_fund_ownership_table_column_names(fund_ownership_record)
        array = convert_date_fields(standard_table, FUND_OWNERSHIP.names)
        table = pa.Table.from_arrays([[a] for a in array], schema=FUND_OWNERSHIP)
        result.append(table)

    return pa.concat_tables(result) if result else None


def to_institutional_ownership_table_column_names(data: dict) -> dict:
    return {new_column_name: data[column_name] for column_name, new_column_name in
            FINNHUB_OWNER_TO_INSTITUTIONAL_OWNERSHIP_TABLE_MAP.items()}


def normalize_instituonal_data(data: dict):
    cusip = data["cusip"]
    symbol = data["symbol"]
    result = []
    for ownership_record in data["data"]:
        report_date = ownership_record["reportDate"]
        for owner in ownership_record["ownership"]:
            record = {"cusip": cusip, "symbol": symbol, "reportDate": report_date}
            record |= owner
            result.append(record)
    return result


def to_institutional_ownership_table(data: dict) -> Optional[pa.Table]:
    result = []
    data = normalize_instituonal_data(data)
    for institutional_ownership_record in data:
        standard_table = to_institutional_ownership_table_column_names(institutional_ownership_record)
        array = convert_date_fields(standard_table, INSTITUTIONAL_OWNERSHIP.names)
        table = pa.Table.from_arrays([[a] for a in array], schema=INSTITUTIONAL_OWNERSHIP)
        result.append(table)
    return pa.concat_tables(result) if result else None


def to_insider_table_column_names(data: dict) -> dict:
    return {new_column_name: data[column_name] for column_name, new_column_name in
            FINNHUB_INSIDER_TO_INSIDER_TABLE_MAP.items()}


def to_insider_table(data: List[dict]) -> Optional[pa.Table]:
    result = []
    for insider_record in data:
        standard_table = to_insider_table_column_names(insider_record)
        array = convert_date_fields(standard_table, INSIDER_TRANSACTION.names)
        table = pa.Table.from_arrays([[a] for a in array], schema=INSIDER_TRANSACTION)
        result.append(table)
    return pa.concat_tables(result) if result else None


def to_dividend_table_column_names(data: dict) -> dict:
    return {new_column_name: data[column_name] for column_name, new_column_name in
            FINNHUB_DIVIDEND_TO_DIVIDEND_TABLE_MAP.items()}


def to_dividend_table(data: List[dict]) -> Optional[pa.Table]:
    result = []
    for dividend_record in data:
        standard_table = to_dividend_table_column_names(dividend_record)
        array = convert_date_fields(standard_table, DIVIDEND.names)
        table = pa.Table.from_arrays([[a] for a in array], schema=DIVIDEND)
        result.append(table)
    return pa.concat_tables(result) if result else None


def convert_date_fields(standard_table, field_names):
    array = []
    for field_name in field_names:
        if field_name == 'period' or "date" in field_name:
            converted_date = attempt_conversion_to_date(field_name, standard_table)
            array.append(converted_date)
        else:
            array.append(standard_table[field_name])
    return array


def attempt_conversion_to_date(name, standard_table):
    try:
        converted_date = int(pd.to_datetime(standard_table[name]).timestamp())
    except Exception as e:
        logger.exception(e)
        logger.info(f"Failed to convert date field for {name}")
        logger.info(standard_table)
        converted_date = None
    return converted_date


def to_ohcl_table_column_names(data, symbol):
    result = {}
    len_n = 0
    for column_name, new_column_name in FINNHUB_CANDLES_TO_OHCL_TABLE_MAP.items():
        result[new_column_name] = data[column_name]
        if len_n == 0:
            len_n = len(result[new_column_name])
            result["symbol"] = [symbol] * len_n
    return result


def to_ohcl_table(finnhub_dict_data: dict, symbol: str) -> pa.Table:
    standard_table = to_ohcl_table_column_names(finnhub_dict_data, symbol)
    return pa.Table.from_arrays([standard_table[name] for name in OHCL.names], schema=OHCL)


def to_company_table_column_names(data):
    return {new_column_name: data[column_name] for column_name, new_column_name in
            FINNHUB_COMPANY_NAME_TO_COMPANY_DESCRIPTION.items()}


def to_company_description_table(finnhub_dict_data: dict):
    try:
        table = to_company_table_column_names(finnhub_dict_data)
        if table["ipo"]:
            table["ipo"] = pd.to_datetime(table["ipo"]).timestamp()
        else:
            table["ipo"] = None
    except Exception as e:
        logger.exception(e)
        raise e
    return pa.Table.from_arrays([[table[name]] for name in COMPANY_PROFILE.names], schema=COMPANY_PROFILE)


def to_standard_column_names(financials, column_name_map: Dict[str, str]):
    return {new_column_name: financials.get(column_name, 0) for column_name, new_column_name in
            column_name_map.items()}


def to_balance_sheet_financial_data(financial_records) -> Optional[pa.Table]:
    if not (financials := financial_records["financials"]):
        return

    symbol = financial_records["symbol"]
    result = []
    for financial_record in financials:
        financial_record["symbol"] = symbol
        standard_table = to_standard_column_names(financial_record,
                                                  FINNHUB_BALANCE_SHEET_TO_BALANCE_SHEET_TABLE)
        array = convert_date_fields(standard_table, BALANCE_SHEET.names)
        table = pa.Table.from_arrays(
            [[a] for a in array],
            schema=BALANCE_SHEET,
        )
        result.append(table)

    return pa.concat_tables(result) if result else None


def to_income_statement_financial_data(financial_records) -> Optional[pa.Table]:
    if not (financials := financial_records["financials"]):
        return

    symbol = financial_records["symbol"]
    result = []
    for financial_record in financials:
        financial_record["symbol"] = symbol
        standard_table = to_standard_column_names(financial_record,
                                                  FINNHUB_INCOME_STATEMENT_TO_INCOME_STATEMENT_TABLE)
        array = convert_date_fields(standard_table, INCOME_STATEMENT.names)
        table = pa.Table.from_arrays(
            [[a] for a in array],
            schema=INCOME_STATEMENT,
        )
        result.append(table)

    return pa.concat_tables(result) if result else None


def to_cash_flow_financial_data(financial_records) -> Optional[pa.Table]:
    if not (financials := financial_records["financials"]):
        return
    symbol = financial_records["symbol"]
    result = []
    for financial_record in financials:
        financial_record["symbol"] = symbol
        standard_table = to_standard_column_names(financial_record,
                                                  FINNHUB_CASHFLOW_STATEMENT_TO_CASHFLOW_STATEMENT_TABLE)
        array = convert_date_fields(standard_table, CASHFLOW_STATEMENT.names)
        table = pa.Table.from_arrays([[a] for a in array], schema=CASHFLOW_STATEMENT)
        result.append(table)
    return pa.concat_tables(result) if result else None


def to_split_data(splits: dict, symbol: str) -> Optional[pa.Table]:
    if not splits:
        return

    result = []
    for split in splits:
        split["symbol"] = symbol
        standard_table = to_standard_column_names(split, FINNHUB_SPLIT_TO_SPLIT_TABLE)
        array = convert_date_fields(standard_table, SPLIT.names)
        if table := pa.Table.from_arrays([[a] for a in array], schema=SPLIT):
            result.append(table)
    return pa.concat_tables(result) if result else None


def to_all_owners_table(all_owners_table):
    if not (owners := all_owners_table["ownership"]):
        return
    symbol = all_owners_table["symbol"]
    result = []
    for owner in owners:
        owner["symbol"] = symbol
        standard_table = to_standard_column_names(owner, FINNHUB_OWNER_TO_OWNER_TABLE)
        array = convert_date_fields(standard_table, OWNER.names)
        if table := pa.Table.from_arrays([[a] for a in array], schema=OWNER):
            result.append(table)
    return pa.concat_tables(result) if result else None
