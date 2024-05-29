import datetime as dt
import yfinance as yfin
import pandas as pd
import MetaTrader5 as mt5
from vnstock import stock_historical_data
from pandas_datareader import data as pdr

def get_crypto(crypto_currency, date_start, date_end=None):
    """
    Truy xuất dữ liệu lịch sử cho một loại tiền điện tử cụ thể trong đơn vị USD từ Yahoo.finance.
    
    Tham số:
        crypto_currency (str): Ký hiệu hoặc tên của tiền điện tử.
        date_start (str hoặc datetime): Ngày bắt đầu cho dữ liệu lịch sử. Định dạng: 'YYYY-MM-DD'.
        date_end (str hoặc datetime, tùy chọn): Ngày kết thúc cho dữ liệu lịch sử. Nếu không được cung cấp, mặc định là ngày hiện tại.
        
    Trả về:
        pandas.DataFrame: DataFrame chứa dữ liệu lịch sử của tiền điện tử.
    """
    yfin.pdr_override()
    if date_end is None:
        date_end = dt.datetime.now()
    df = pdr.get_data_yahoo(crypto_currency, start=date_start, end=date_end)
    return df

def get_vnstock(symbol, resolution, type, start_date, end_date=None, beautify=False, decor=False, source='DNSE'):
    """
    Truy xuất dữ liệu lịch sử cho một mã cổ phiếu cụ thể từ thị trường chứng khoán Việt Nam.

    Tham số:
        symbol (str): Ký hiệu của cổ phiếu.
        resolution (str): Độ phân giải của dữ liệu. Ví dụ: 'D' cho hàng ngày, 'W' cho hàng tuần.
        type (str): Loại dữ liệu. Ví dụ: 'line' hoặc 'candle'.
        start_date (str hoặc datetime): Ngày bắt đầu cho dữ liệu lịch sử. Định dạng: 'YYYY-MM-DD'.
        end_date (str hoặc datetime, tùy chọn): Ngày kết thúc cho dữ liệu lịch sử. Nếu không được cung cấp, mặc định là ngày hiện tại.
        beautify (bool, tùy chọn): Có beautify dữ liệu hay không. Mặc định là False.
        decor (bool, tùy chọn): Có thêm trang trí cho dữ liệu hay không. Mặc định là False.
        source (str, tùy chọn): Nguồn dữ liệu. Mặc định là 'DNSE'.
        
    Trả về:
        pandas.DataFrame: DataFrame chứa dữ liệu lịch sử của cổ phiếu.
    """
    if end_date is None:
        end_date = dt.datetime.now()
    df =  stock_historical_data(symbol=symbol, 
                            start_date=str(start_date)[0:10], 
                            end_date=str(end_date)[0:10], resolution=resolution, type=type, beautify=beautify, decor=decor, source=source)
    return df

def get_forex(pair, date_start, date_end, login=None, password=None, server=None):
    """
    Truy xuất dữ liệu lịch sử cho một cặp tiền từ nền tảng MetaTrader 5.

    Tham số:
        pair (str): Ký hiệu cặp tiền. Ví dụ: 'EURUSD'.
        date_start (str hoặc datetime): Ngày bắt đầu cho dữ liệu lịch sử. Định dạng: 'YYYY-MM-DD'.
        date_end (str hoặc datetime): Ngày kết thúc cho dữ liệu lịch sử. Định dạng: 'YYYY-MM-DD'.
        login (str, tùy chọn): ID đăng nhập của MetaTrader 5. Yêu cầu nếu password và server được cung cấp.
        password (str, tùy chọn): Mật khẩu tài khoản MetaTrader 5. Yêu cầu nếu login và server được cung cấp.
        server (str, tùy chọn): Tên máy chủ MetaTrader 5. Yêu cầu nếu login và password được cung cấp.
        
    Trả về:
        pandas.DataFrame: DataFrame chứa dữ liệu lịch sử của forex.
    """
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    if login and password and server:
        mt5.login(login, password, server)
    rates = mt5.copy_rates_range(pair, mt5.TIMEFRAME_M15, date_start, date_end)
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df = df.rename(columns={'time': 'Date', 'open': 'Open',
                   'low': 'Low', 'close': 'Close', 'high': 'High', 'tick_volume': 'Volume'})
    mt5.shutdown()
    return df
