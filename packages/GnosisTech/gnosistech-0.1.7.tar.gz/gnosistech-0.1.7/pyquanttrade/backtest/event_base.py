from _backtest_source.source import Backtest, Strategy

def use_changes(data, changes):
    """
    Sử dụng chiến lược dựa trên thay đổi giá và thực hiện backtest.

    Parameters:
        data (DataFrame): Dữ liệu chứa giá.

    Returns:
        tuple: Thống kê và kết quả backtest.
    """
    class ChangesStrategy(Strategy):
        """
        Chiến lược sử dụng thay đổi giá để giao dịch.

        """

        def init(self):
            pass

        def next(self):
            current_signal = self.data.Changes

            if current_signal > 0:
                if not self.position:
                    self.buy()  
            elif current_signal < 0:
                if self.position:
                    self.position.close()

    data['Changes'] = changes 
    bt = Backtest(data, ChangesStrategy, exclusive_orders=True)
    stats = bt.run()
    return stats, bt
