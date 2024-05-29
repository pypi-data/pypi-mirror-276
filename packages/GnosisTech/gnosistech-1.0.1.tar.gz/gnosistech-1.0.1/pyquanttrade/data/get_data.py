import datetime as dt
import yfinance as yfin
import pandas as pd
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

