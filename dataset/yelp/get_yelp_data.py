import json
import argparse
import requests
#packages for csv management
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(override=True)
API_KEY = os.getenv("YELP_API_KEY")

#this is a script to gather the restaurants using the yelp API
url = "https://api.yelp.com/v3/businesses/search?"
headers = {"Authorization": "Bearer %s" % API_KEY}
offset = 0
parameters = {"location":'chicago%2C2%0IL',"term":"restaurants", "limit": 50, "offset":offset}


def call_api(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    return(response)

'''
#hardcoded url
my_url = "https://api.yelp.com/v3/businesses/search?location=chicago%2C%20IL&term=restaurants&sort_by=best_match&limit=25"
chicago_rests = requests.get(my_url, headers=headers)
print(chicago_rests.text)
'''
# path to store sample dataset
chicago_rest_path = Path("/Users/samanthabastien/Desktop/Desktop - Samantha’s MacBook Pro/fall 2023/tastebudz/repository/tastebudz/dataset/yelp_dataset/chicago_restaurants.csv")
restaurant_df = pd.DataFrame()


#get data
for i in range(1, 20):
    temp_response = call_api(url, headers=headers, params=parameters)
    data = temp_response.json()
    temp_df = pd.DataFrame(data["businesses"])
    selected_columns = ["id", "name", "review_count", "categories", "rating", "coordinates", "price", "location",]
    # ["id", "alias", "name","image_url","is_closed","url","review_count","categories", "rating", "coordinates", "transactions", "price", "location", "phone", "display_phone", "distance"]
    temp_df= temp_df[selected_columns]
    restaurant_df = restaurant_df.append(temp_df, ignore_index=True)
    offset +=50

#save to csv
restaurant_df.to_csv(chicago_rest_path)