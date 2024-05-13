import pandas as pd
import numpy as np
import yfinance as yf

ticker_data = pd.read_csv('share_df.csv')

tickers = np.unique(ticker_data['Ticker']).tolist()

hist_data = []
cols = ['Date','Open','Close','High','Low','Volume','Ticker']

for t in tickers:
    s = yf.Ticker(t)
    hist = s.history(period="1mo")
    hist = hist.drop(columns=['Dividends','Stock Splits'])
    hist.drop(hist.tail(1).index, inplace=True)

    
    ind = 0
    
    for index,row in hist.iterrows():
        s_data=[]

        s_data.append(hist.index[ind].to_pydatetime().date())
        s_data.append(row['Open'])
        s_data.append(row['Close'])
        s_data.append(row['High'])
        s_data.append(row['Low'])
        s_data.append(row['Volume'])
        s_data.append(t)

        
    
        ind = ind + 1
    
        hist_data.append(s_data)
        
hist_df = pd.DataFrame(hist_data,columns=cols)

hist_df.to_csv('hist_df_1month_6.csv',index=False)#PXD removed from SP500, bought by exxon mobile
