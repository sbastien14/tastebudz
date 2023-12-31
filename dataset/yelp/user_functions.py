from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from os import path
import random

cur_dir = path.dirname(__file__)
clean_data = path.join(cur_dir, "clean_data.csv")
reco = path.join(cur_dir, "recommend_data.csv")

clean_data_df = pd.read_csv(clean_data)
reco_df = pd.read_csv(reco)
cos_sim = cosine_similarity(reco_df, reco_df)

#function to fetch recommendations
def fetch_recos(current_user):
    restaurant_name = current_user.swiped_restaurants.random.choice()
    index = clean_data_df[clean_data_df['name'] == restaurant_name].index
    indices = cos_sim[index][0].argsort()[::-1]

    #fill short stack to 10 places
    while len(current_user.short_stack) <= 10:
        for ind in indices:
            #ensure that the places added to the stack haven't been seen
            if ind != index and ind not in current_user.swiped_restaurants:
                current_user.short_stack.append(clean_data_df.iloc[ind])
    # return push short_stack to website
    return()

# Rewritten to not rely on structure of the user object here.
#   likedRestaurants is a list of Yelp Restaurant IDs.
#   Returns a list of Yelp Restaurant IDs.
def getRecommendations(likedRestaurants:list) -> list:
    short_stack:list = []
    
    # Just give some random recommendations if no likes exist:
    if len(likedRestaurants) == 0:
        short_stack = list(clean_data_df.sample(n=10).id)
    # Otherwise use some ML:
    else:
        restaurant_id = random.choice(likedRestaurants)
        index = clean_data_df[clean_data_df['id'] == restaurant_id].index
        
        if not index.empty:
            index = index[0]
            indices = cos_sim[index].argsort()[::-1]
            for ind in indices:
                if ind != index:
                    if clean_data_df.iloc[ind]['id'] not in short_stack:
                        short_stack.append(clean_data_df.iloc[ind]['id'])
                    if len(short_stack) == 11:
                        break
        short_stack.pop(0)
    
    return short_stack
'''
#function to check if a restaurant is within the user's radius
def check_bounds(restaurant):
    # write function

# function to create distance importance values
# do upon start of session
def calc_distance_importance(current_user):
    for restaurant in reco_df:
        if restaurant.lat: current_user.current_loction

'''