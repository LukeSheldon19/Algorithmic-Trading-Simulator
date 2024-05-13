import argparse
import random
import csv
import os
import pandas as pd

import django
from django.db import transaction
from django.utils import timezone

django.setup()

from myApp.models import Company, Share, Data, Portfolio, Composed_of

def main():

    df = pd.read_csv('hist_df_1month_6.csv')

    with transaction.atomic():

        datas = []

        for index, row in df.iterrows():

            datas.append(Data(index,row['Date'],row['Open'],row['Close'],row['High'],row['Low'],row['Volume'],row['Ticker']))

    Data.objects.bulk_create(datas)


if __name__ == "__main__":
    main()
