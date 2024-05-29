import pandas as pd
from _backtest_source.source import Backtest, Strategy
from _backtest_source.lib import SignalStrategy, TrailingStrategy

def use_position(data, pos_array):
    """
    Sử dụng tín hiệu mua/bán từ một mảng và thực hiện backtest.

    Parameters:
        data (DataFrame): Dữ liệu chứa giá và tín hiệu.
        pos_array (array-like): Mảng chứa tín hiệu mua/bán (1/-1).

    Returns:
        tuple: Thống kê và kết quả backtest.
    """

    class PosStrategy(Strategy):
        """
        Chiến lược sử dụng tín hiệu mua/bán để giao dịch.

        """

        def init(self):
            pass
        
        def next(self):
            current_signal = self.data.Signal

            if current_signal == 1:
                if not self.position:
                    self.buy()       
            elif current_signal == -1:
                if self.position:
                    self.position.close()

    pos_array.index = data.index
    data['Signal'] = pos_array
    bt = Backtest(data, PosStrategy)
    stats = bt.run()
    return stats, bt

def use_signal_ma(data, ma1, ma2):
    """
    Sử dụng chiến lược dựa trên tín hiệu của moving average và thực hiện backtest.

    Parameters:
        data (DataFrame): Dữ liệu chứa giá và tín hiệu.
        ma1 (Int): thời gian chu kỳ moving average đầu tiên của giá Close
        ma2 (Int): thời gian chu kỳ moving average thứ 2 của giá Close

    Trả về:
        stats (dict): Thống kê của kiểm thử.
        bt (Backtest): Hình vẽ của kiểm thử.
    """

    def SMA(arr: pd.Series, n: int) -> pd.Series:
        """
        Trả về thời gian chu kỳ moving average của một array `arr`.
        """
        return pd.Series(arr).rolling(n).mean()

    class MASignal(SignalStrategy):
            """

            Chiến lược sử dụng tín hiệu moving average để giao dịch.

            """
            def init(self):
                super().init()
                price = self.data.Close
                self.ma1 = self.I(SMA, price, ma1)
                self.ma2 = self.I(SMA, price, ma2)
                self.set_signal(self.ma1 > self.ma2, self.ma1 < self.ma2)
            
            def next(self):
                 super().next()
                
    bt = Backtest(data, MASignal)
    stats = bt.run()
    return stats, bt

def use_trailing(data, atr_periods, trailing_sl, rolling):
    """
    Thực hiện kiểm thử chiến lược giao dịch sử dụng trailing stop-loss.
    
    Hàm này khởi tạo và chạy một kiểm thử giao dịch cho một chiến lược sử dụng trailing stop-loss.

    Tham số:
        data (DataFrame): Dữ liệu giá lịch sử bao gồm giá Open, High, Low, Close.
        atr_periods (int): Số kỳ tính toán Average True Range (ATR).
        trailing_sl (int): Kích thước trailing stop-loss theo đơn vị ATR.
        rolling (int): Số kỳ cho cửa sổ trượt.

    Trả về:
        stats (dict): Thống kê của kiểm thử.
        bt (Backtest): Hình vẽ của kiểm thử.
    """

    class SLTrailling(TrailingStrategy):
        """
        Chiến lược giao dịch mẫu sử dụng trailing stop-loss.
        """

        def init(self):
            """
            Khởi tạo các tham số chiến lược và chỉ báo.
            """
            super().init()
            self.set_atr_periods(atr_periods)
            self.set_trailing_sl(trailing_sl)
            self.sma = self.I(lambda: self.data.Close.s.rolling(rolling).mean())

        def next(self):
            """
            Thực hiện logic giao dịch trên mỗi điểm dữ liệu mới.
            """
            super().next()
            if not self.position and self.data.Close > self.sma:
                self.buy()

    # Khởi tạo và chạy kiểm thử
    bt = Backtest(data, SLTrailling)
    stats = bt.run()

    return stats, bt
