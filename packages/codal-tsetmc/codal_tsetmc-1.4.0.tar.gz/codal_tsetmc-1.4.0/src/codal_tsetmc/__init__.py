import os
from sqlalchemy.sql import text

from codal_tsetmc.config.engine import (
    HOME_PATH, CDL_TSE_FOLDER, default_db_path, CONFIG_PATH
)
from codal_tsetmc.tools.database import (
    read_table_by_conditions, read_table_by_sql_query, fill_table_of_db_with_df
)
from codal_tsetmc.models.stocks import (
    Stocks, StocksPrices, StocksCapitals, StocksGroups, CommoditiesPrices
)
from codal_tsetmc.models.companies import (
    Companies, CompanyTypes, CompanyStatuses, LetterTypes, Letters, FinancialYears,
    FinancialStatementHeader, FinancialStatementTableWithSingleItem,
)
from codal_tsetmc.download.codal.query import CodalQuery
from codal_tsetmc.download.tsetmc.price import (
    update_stocks_group_prices,
    update_stocks_prices,
    update_stock_prices
)
from codal_tsetmc.download.tsetmc.stock import (
    get_stock_ids,
    update_stocks_table,
    get_stocks_groups,
    get_stock_detail,
)
from codal_tsetmc.download.tsetmc.capital import (
    get_stock_capitals_history, get_stock_capital_daily,
    update_stock_capitals, update_stocks_capitals, update_stocks_group_capitals
)

from .config import engine as db
from .initializer import (
    create_db,
    init_db,
    fill_db,
    fill_companies_table,
    fill_categories_table,
    fill_stocks_groups_table,
    fill_stocks_table,
    fill_stocks_prices_table,
    fill_stocks_capitals_table,
    fill_commodities_prices_table,
)


def db_is_empty():
    try:
        for table in [
            "companies", "company_types", "company_statuses",
            "report_types", "letter_types", "auditors",
            "financial_years", "stocks_groups", "stocks"
        ]:
            db.session.execute(text(f"select * from {table} limit 1;"))

        return False
    except Exception as e:
        print("db_is_empty: ", e.__context__, end="\r", flush=True)
        return True


if db_is_empty():
    create_db()
    init_db()
