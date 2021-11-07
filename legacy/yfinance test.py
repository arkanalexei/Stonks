import yfinance as yf
import numpy as np
spy = yf.Ticker('SPY')



urls=[
'spy'
    ]

#for url in urls:


 #   np.savetxt('spydata.csv', spy.history(period='max'), delimiter = ',')


print(spy.history(period='10y'))

