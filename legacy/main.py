import numpy as np
import backtrader as bt
import datetime

from GoldenCross import GoldenCross
import matplotlib.pyplot as plt



cerebro = bt.Cerebro()
cerebro.broker.setcash(100)

data = bt.feeds.YahooFinanceCSVData(
    dataname='spy.csv',
    # Do not pass values before this date
    fromdate=datetime.datetime(1990, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2022, 1, 1),
    reverse=False)

cerebro.adddata(data)

cerebro.addstrategy(GoldenCross)



print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()