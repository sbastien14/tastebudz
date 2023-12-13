from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    session, current_app
)
from tastebudz.auth import login_required
from tastebudz.gmaps import get_gmaps
from tastebudz.yelp_api import get_yelp
from tastebudz.auth import get_sb
from tastebudz.models import Restaurant, User
from dataset.yelp.user_functions import getRecommendations
import logging

bp = Blueprint('restaurant', __name__)

@bp.before_app_request
def load_logged_in_user():
    sb = get_sb()
    res = sb.auth.get_user()
    if res is not None:
        g.user = User(res.user)
    else:
        g.user = None


def getRestaurant(restaurantId:str):
    try:
        r = Restaurant(restaurantId)
        response = { "restaurant": r }
        statusCode = 200
    except Exception as error:
        response = { "message": f"{type(error)}: {str(error)}" }
        statusCode = 500
    
    return response, statusCode


@login_required
def swipe(restaurantId:str, direction:str):
    try:
        print(g.user)
        r = Restaurant(restaurantId)
        g.user.swipe(r, direction)
        response = { "restaurant": r }
        statusCode = 200
    except Exception as error:
        response = { "message": f"{type(error)}: {str(error)}" }
        statusCode = 500
        
    return response, statusCode


@login_required
def getRec():
    #  Try to retrieve recommendation from session:
    if "recommendations" in session:
        # Get a recommendation and generate a Restaurant object from it:
        try:
            newRec = Restaurant(session["recommendations"][-1])
            session["recommendations"] = session["recommendations"][:-1]
        except Exception as error:
            logging.getLogger().error(f"[RESTAURANT/GETREC] Failed to get recommendation from session. {type(error)}: {str(error)}")
            response = { "message": f"{type(error)}: {str(error)}" }
            statusCode = 500
        else:
            response = { "restaurant": newRec }
            statusCode = 200
            
        # Generate new recommendations if needed and store Yelp Restaurant IDs in session:
        if len(session["recommendations"]) < current_app.config["TASTEBUDZ_REC_GEN_THRESHOLD"]:
            try:
                session["recommendations"].extend(getRecommendations(g.user.right_swipes))
                logging.getLogger().info("[RESTAURANT/GETREC] Generated new recommendations.")
            except Exception as error:
                logging.getLogger().error(f"[RESTAURANT/GETREC] Failed to generate new recommendations. {type(error)}: {str(error)}")
            
    # Otherwise, generate new recommendations and put them in our session:
    else:
        try:
            session["recommendations"] = getRecommendations(g.user.right_swipes)
            logging.getLogger().info("[RESTAURANT/GETREC] Generated new recommendations.")
        except Exception as error:
            logging.getLogger().error(f"[RESTAURANT/GETREC] Failed to generate recommendations. {type(error)}: {str(error)}")
            response = { "message": f"{type(error)}: {str(error)}" }
            statusCode = 500

        # Get a recommendation and generate a Restaurant object from it:
        try:
            newRec = Restaurant(session["recommendations"][-1])
            session["recommendations"].pop()
        except Exception as error:
            logging.getLogger().error(f"[RESTAURANT/GETREC] Failed to get recommendation from session. {type(error)}: {str(error)}")
            response = { "message": f"{type(error)}: {str(error)}" }
            statusCode = 500
        else:
            response = { "restaurant": newRec }
            statusCode = 200
    print(session["recommendations"])
    
    return response, statusCode
            

# def getRestaurant(gmaps, img=True):
#     # Attributes of interest to filter by:
#     #   - dine_in
#     #   - open_now
#     #   - price_level
#     #   - rating
#     #   - serves_beer
#     #   - serves_breakfast
#     #   - serves_brunch
#     #   - serves_lunch
#     #   - serves_dinner
#     #   - serves_wine
#     #   - types (see https://developers.google.com/places/supported_types)
#     search = gmaps.places(type="restaurant", open_now=True)
#     restaurant = gmaps.place(search["results"][random.randrange(len(search["results"]))]["place_id"])["result"]
#     name = restaurant["name"]
#     address = restaurant["formatted_address"]
#     if img:
#         photo = f'{restaurant["photos"][0]["photo_reference"]}.png'
#         try:
#             open(f'tastebudz/static/{photo}', 'r')
#         except:
#             f = open(f'tastebudz/static/{photo}', 'wb')
#             for chunk in gmaps.places_photo(restaurant["photos"][0]["photo_reference"], max_height=500):
#                 if chunk:
#                     f.write(chunk)
#             f.close()
#     else:
#         photo = ""
#     return name, address, photo, restaurant