# this is a python script to clean the data from kaggle
import numpy as np
import pandas as pd
from pandas import dataframe as df
import geopy as gp
import os
import csv
cleaned_data = "/Users/samanthabastien/Desktop/Desktop - Samantha’s MacBook Pro/fall 2023/tastebudz/repository/tastebudz/dataset/archive/cleaned_data.csv"
original_data = "/Users/samanthabastien/Desktop/Desktop - Samantha’s MacBook Pro/fall 2023/tastebudz/repository/tastebudz/dataset/archive/restaurants.csv"

cuisine_types = []

#drops restaurants with no ratings and/or number of reviews
if os.path.exists(cleaned_data) is False:
    with open(original_data, "r") as od:
        with open(cleaned_data, "w+") as cd:
            reader = csv.reader(od)
            writer = csv.writer(cd)
            for row in reader:
                if not row[3] or not row[4]:
                    continue
                else:
                    writer.writerow(row)
        cd.close()
    od.close()

data = pd.read_csv(cleaned_data)
data.drop('position')

