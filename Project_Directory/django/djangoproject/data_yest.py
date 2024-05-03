import argparse
import random
import csv
import os
import pandas as pd
import yfinance as yf 
import datetime


import django
from django.db import transaction
from django.utils import timezone
from django.db.models import Max


django.setup()

from myApp.models import Company, Share, Data, Portfolio, Composed_of

def main():

    df = pd.read_csv('share_df.csv')

    prev_day = []

    for t in df['Ticker']:
        s = yf.Ticker(t)
        hist = s.history(period="2d")

        if len(hist) > 1:
    
            hist.drop(hist.index[1], inplace=True)
            hist['Date'] = hist.index[0].date()
            hist['Date'] = hist['Date'].astype(str)
            hist.reset_index(drop=True, inplace=True)
            hist = hist.drop(columns=['Dividends','Stock Splits'])
            hist['Ticker'] = t
            prev_day.append(hist)
        else:

            hist['Date'] = hist.index[0].date()
            hist['Date'] = hist['Date'].astype(str)
            hist.reset_index(drop=True, inplace=True)
            hist = hist.drop(columns=['Dividends','Stock Splits'])
            hist['Ticker'] = t
            prev_day.append(hist)



    with transaction.atomic():
        
        new_data = []

        largest_index = Data.objects.aggregate(largest_index=Max('id'))['largest_index']

        inc_id = largest_index

        for r in prev_day:
            t = r['Ticker'][0]
            oldest_data = Data.objects.filter(ticker=t).order_by('id').first()
            if oldest_data:
                oldest_data.delete()

            #largest_index = Data.objects.aggregate(largest_index=Max('id'))['largest_index']

            inc_id = inc_id + 1

            st = Data(inc_id,r['Date'][0],r['Open'][0],r['Close'][0],r['High'][0],r['Low'][0],r['Volume'][0],r['Ticker'][0])

            new_data.append(st)

        Data.objects.bulk_create(new_data)



if __name__ == "__main__":
    main()
        