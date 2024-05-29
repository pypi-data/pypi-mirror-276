import os
from sqlalchemy.sql import text

from codal_tsetmc.config.engine import HOME_PATH, CDL_TSE_FOLDER, default_db_path, CONFIG_PATH
from codal_tsetmc.tools.database import read_table_by_conditions, read_table_by_sql_query
from codal_tsetmc.models.stocks import Stocks
from codal_tsetmc.models.companies import Companies
from codal_tsetmc.download.codal.query import CodalQuery

from .config import engine as db
from .initializer import (
    create_db,
    init_db,
    fill_db,
    fill_companies_table,
    fill_categories_table,
    fill_stocks_table,
    update_stocks_group_prices,
    fill_stocks_prices_table,
    fill_stocks_capitals_table,
    fill_commodities_prices_table,
)


def db_is_empty():
    try:
        for table in [
            "companies", "company_types", "company_statuses",
            "report_types", "letter_types", "auditors", "financial_years",
            "stocks"
        ]:
            db.session.execute(text(f"select * from {table} limit 1;"))

        return False
    except Exception as e:
        print(e.__context__)
        return True
    finally:
        pass


if db_is_empty():
    create_db()
    init_db()
