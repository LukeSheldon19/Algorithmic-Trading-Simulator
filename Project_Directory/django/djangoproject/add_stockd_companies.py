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

    df = pd.read_csv('companies_unique.csv')

    with transaction.atomic():

        comps = []

        for index, row in df.iterrows():

            comps.append(Company(index, row['Name'], row['Sector'], row['Num_Employees'], row['Industry'], row['End_Fiscal_Year']))


    Company.objects.bulk_create(comps)


if __name__ == "__main__":
    main()
