from codal_tsetmc.config.engine import engine
from codal_tsetmc.models.stocks import (
    Stocks,
    StockPrice,
    StockCapital,
    CommodityPrice
)
from codal_tsetmc.models.companies import (
    Companies,
    CompanyTypes,
    CompanyStatuses,
    FinancialYears,
    ReportTypes,
    LetterTypes,
    Auditors,
    Letters,
    FinancialStatementHeader,
    FinancialStatementTableWithSingleItem
)

models = [
    Stocks,
    StockPrice,
    StockCapital,
    Companies,
    CompanyTypes,
    CompanyStatuses,
    FinancialYears,
    ReportTypes,
    LetterTypes,
    Auditors,
    Letters,
    FinancialStatementHeader,
    FinancialStatementTableWithSingleItem,
    CommodityPrice
]


def create_table(model):
    try:
        model.__table__.create(engine)
    except Exception as e:
        print(e.__context__)
    finally:
        pass


def create():
    for model in models:
        create_table(model)
