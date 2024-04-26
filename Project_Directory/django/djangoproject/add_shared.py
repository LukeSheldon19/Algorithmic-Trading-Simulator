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

    df = pd.read_csv('share_df.csv')

    with transaction.atomic():

        shares = []

        for index, row in df.iterrows():

            shares.append(Share(row['Ticker'],row['Type'],index))

    Share.objects.bulk_create(shares)


if __name__ == "__main__":
    main()
