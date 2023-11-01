from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

clean_data = "/Users/samanthabastien/Desktop/Desktop - Samantha’s MacBook Pro/fall 2023/tastebudz/repository/tastebudz/dataset/yelp_dataset/clean_data.csv"
reco = "/Users/samanthabastien/Desktop/Desktop - Samantha’s MacBook Pro/fall 2023/tastebudz/repository/tastebudz/dataset/yelp_dataset/recommend_data.csv"

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

#function to check if a restaurant is within the user's radius
def check_bounds(restaurant):
    if

# function to create distance importance values
# do upon start of session
def calc_distance_importance(current_user):
    for restaurant in reco_df:
        if restaurant.lat current_user.current_loction