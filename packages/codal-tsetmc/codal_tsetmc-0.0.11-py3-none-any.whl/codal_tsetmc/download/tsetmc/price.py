from jdatetime import datetime as jdt
from datetime import datetime
import jalali_pandas
import aiohttp
import pandas as pd
import io
import requests
from codal_tsetmc.config.engine import session
from codal_tsetmc.models.stocks import Stocks
from codal_tsetmc.tools.database import (
    fill_table_of_db_with_df,
    read_table_by_conditions
)
from codal_tsetmc.tools.api import (
    get_data_from_cdn_tsetmec_api,
    get_results_by_asyncio_loop
)
from codal_tsetmc.download.tsetmc.stock import (
    is_stock_in_akhza_bond,
    is_stock_in_gam_bond,
    is_stock_in_bourse_or_fara_or_paye
)

INDEX_CODE = "32097828799138957"


def get_index_prices_history():
    url = f'http://cdn.tsetmc.com/api/Index/GetIndexB2History/{INDEX_CODE}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 '
                      'Safari/537.36',
    }
    s = requests.get(url, headers=headers, verify=False).json()
    df = pd.DataFrame(s["indexB2"])[["dEven", "xNivInuClMresIbs"]]
    df.columns = ["date", "price"]
    df["date"] = df["date"].apply(lambda x: datetime.strptime(str(x), "%Y%m%d"))
    df["date"] = df["date"].jalali.to_jalali().apply(lambda x: x.strftime('%Y%m%d000000'))
    df["code"] = INDEX_CODE
    df["symbol"] = "شاخص كل6"
    df["value"] = pd.NA
    df["volume"] = pd.NA
    df = df.sort_values("date")

    return df


def update_index_prices():
    df = get_index_prices_history()
    df["up_date"] = jdt.now().strftime("%Y%m%d000000")
    fill_table_of_db_with_df(
        df[["date", "symbol", "code", "price", "volume", "value", "up_date"]],
        columns="date",
        table="stock_price",
        conditions=f"where code = '{INDEX_CODE}'",
        text=f"stock: {INDEX_CODE}"
    )


def get_stock_price_daily(code: str, date: str):
    data = "ClosingPrice/GetClosingPriceDaily"
    dict_data = get_data_from_cdn_tsetmec_api(data, code, date)

    return dict_data["closingPriceDaily"]["pClosing"]


def cleanup_stock_prices_records(data):
    df = pd.read_csv(io.StringIO(data), delimiter="@", lineterminator=";", engine="c", header=None)
    df.columns = "date high low price close open yesterday value volume count".split()
    df["date"] = df["date"].apply(lambda x: datetime.strptime(str(x), "%Y%m%d"))
    df["date"] = df["date"].jalali.to_jalali().apply(lambda x: x.strftime('%Y%m%d000000'))
    df = df.sort_values("date")

    return df[["date", "volume", "value", "price"]]


def get_stock_prices_history(code: str) -> pd.DataFrame:
    url = f"http://old.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={code}&Top=999999&A=0"
    data = requests.get(url).text
    df = pd.read_csv(io.StringIO(data), delimiter="@", lineterminator=";", engine="c", header=None)
    df.columns = "date high low price close open yesterday value volume count".split()
    df["date"] = df["date"].apply(lambda x: datetime.strptime(str(x), "%Y%m%d"))
    df["code"] = code

    return df


async def update_stock_prices(code: str):
    url = ""
    try:
        if not is_stock_in_bourse_or_fara_or_paye(code) and not is_stock_in_akhza_bond(
                code) and not is_stock_in_gam_bond(code):
            return

        now = datetime.now().strftime("%Y%m%d")
        try:

            def get_max_date_stock():
                return read_table_by_conditions(
                    table="stock_price",
                    variable="code",
                    value=code,
                    columns="max(date) AS date"
                )

            def get_max_date_index():
                return read_table_by_conditions(
                    table="stock_price",
                    variable="code",
                    value=INDEX_CODE,
                    columns="max(date) AS date"
                )

            last_date_stock = get_max_date_stock().date.iat[0]
            last_date_index = get_max_date_index().date.iat[0]

            if last_date_index is None or (last_date_stock is not None and int(last_date_index) < int(last_date_stock)):
                update_index_prices()
                last_date_index = get_max_date_index().date.iat[0]

        except Exception as e:
            print(e)
            last_date_stock = "0"
            last_date_index = "0"

        try:
            if last_date_stock is None:  # Not any record added in database
                url = (
                    f"http://old.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={code}&Top=999999&A=0"
                )
            elif int(last_date_stock) < int(last_date_index):  # need to update new price data
                last_date = jdt.strptime(str(int(last_date_stock)), "%Y%m%d%H%M%S").togregorian().strftime("%Y%m%d")
                url = (
                    f"http://old.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={code}&Top=999999&A=0"
                )
            else:  # The price data for this code is updated
                return

        except Exception as e:
            print(f"Error on formatting price:{str(e)}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 '
                          'Safari/537.36'
        }
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url, headers=headers) as resp:
                data = await resp.text()

        df = cleanup_stock_prices_records(data)
        df["code"] = code
        stock = Stocks.query.filter_by(code=code).first()
        df["symbol"] = stock.symbol
        df["up_date"] = jdt.now().strftime("%Y%m%d000000")

        fill_table_of_db_with_df(
            df,
            columns="date",
            table="stock_price",
            conditions=f"where code = '{code}'",
            text=f"stock: {code}"
        )

        return True, code

    except Exception as e:
        return e, code


def update_stocks_prices(codes, msg=""):
    tasks = [update_stock_prices(code) for code in codes]
    get_results_by_asyncio_loop(tasks)
    print(msg, end="\r")
    return True


def update_stocks_group_prices(group_code):
    stocks = session.query(Stocks.code).filter_by(group_code=group_code).all()
    print(f"{' ' * 25} group: {group_code}", end="\r")
    codes = [stock[0] for stock in stocks]
    msg = "group " + group_code + " updated"
    results = update_stocks_prices(codes, msg)
    return results


def fill_stocks_prices_table():
    update_index_prices()
    codes = session.query(Stocks.group_code).distinct().all()
    for i, code in enumerate(codes):
        print(
            f"{' ' * 35} total progress: {100 * (i + 1) / len(codes):.2f}%",
            end="\r",
        )
        update_stocks_group_prices(code[0])
    print("Price Download Finished.", " " * 50)
