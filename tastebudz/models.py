from gotrue.types import User as sbUser
import json, datetime, requests, urllib
from dateutil import parser as dateparser
from tastebudz.sb import get_sb
from tastebudz.yelp_api import get_yelp
from tastebudz.gmaps import get_gmaps

class Restaurant(dict):
    # Populate object with details from Yelp & Google Maps:
    def _fetchDetails(self) -> None:
        y = get_yelp()
        gmaps = get_gmaps()
        
        # Populate data from Yelp:
        business = y.getBusiness(self.id)
        self.id = business.get('id', None)
        self.name = business.get('name')
        self.address = ",".join(business.get('location').get('display_address'))
        self.latitude = business.get('coordinates').get('latitude')
        self.longitude = business.get('coordinates').get('longitude')
        self.phone = business.get('display_phone')
        self.tags = business.get('categories')
        self.yelpUrl = business.get('url')
        self.imgUrl = business.get('image_url')
        
        # Populate data from Google Maps:
        g_data = gmaps.places(query=self.name, location=(self.latitude, self.longitude))
        if len(g_data['results']) > 0:
            place = g_data['results'][0]
            self.googleMapsId = place.get('place_id')
            self.googleMapsUrl = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(self.name)}&query_place_id={self.googleMapsId}"
            
    
    def __init__(self, restaurantId:str):
        self.id:str = restaurantId
        self.name:str = ""
        self.address:str = ""
        self.latitude = ""
        self.longitude = ""
        self.phone:str = ""
        self.tags:list = []
        self.imgUrl:str = ""
        self.googleMapsUrl:str = ""
        self.googleMapsId:str = ""
        self.yelpUrl:str = ""
        
        self._fetchDetails()
        
        # Create instance of dictionary representation:
        self._dict = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "phone": self.phone,
            "tags": self.tags,
            "googleMapsUrl": self.googleMapsUrl,
            "googleMapsId": self.googleMapsId,
            "yelpUrl": self.yelpUrl
        }
        dict.__init__(self, self._dict)


class User(dict):
    def __init__(self, usr):
        if type(usr) == sbUser:
            # Create standard instance variables:
            self.id:str = usr.id
            self.email:str = usr.email
            self.username:str = usr.user_metadata.get('username')
            self.phone:str = usr.phone
            self.role:bool = usr.user_metadata.get('role', 0)
            self.first_name:str = ""
            self.last_name:str = ""
            self.dob:datetime.date = None
            self.friends = []
            self.left_swipes = []
            self.right_swipes = []
            
            # Try to fetch profile data:
            try:
                self.getProfile()
            except Exception as error:
                print(f"{type(error)}: {str(error)}")
        elif type(usr) == dict:
            # Create standard instance variables:
            self.id:str = usr.get('id')
            self.email:str = usr.get('email')
            self.username:str = usr.get('username')
            self.phone:str = usr.get('phone')
            self.role:bool = usr.get('role', 0)
            self.first_name = usr.get('first_name')
            self.last_name = usr.get('last_name')
            self.dob = usr.get('dob')
            self.friends = usr.get('friends')
        else:
            raise Exception("Unexpected type.")
        
        # Create instance of dictionary representation:
        self._dict = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dob": self.dob.isoformat() if self.dob is not None else "",
            "friends": self.friends
        }
        dict.__init__(self, self._dict)
    
    def getProfile(self) -> None:
        sb = get_sb()
        
        # Fetch user profile data from the server.
        try:
            res = sb.table('user_profiles').select('*').eq('username', self.username).execute()
        except:
            res = sb.table('user_profiles').select('*').eq('id', self.id).execute()
        
        if res.data is None or len(res.data) == 0:
            raise SupabaseException("Profile data not found.")
        else:
            profile = res.data[0]
        
        # Update instance data:
        self.first_name = profile.get('first_name')
        self.last_name = profile.get('last_name')
        self.dob = dateparser.parse(profile.get('dob')).date()
        self.friends = profile.get('friends')
        
        # Update internal dictionary:
        self._dict = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "dob": self.dob.isoformat(),
            "friends": self.friends
        }
    
    def createProfile(self, properties:dict={}) -> None:
        sb = get_sb()
        
        # Validation and typecasting:
        if type(properties.get('first_name', "")) is not str:
            raise TypeError("'first_name' must be a string.")
        if type(properties.get('last_name', "")) is not str:
            raise TypeError("'last_name' must be a string.")
        if type(properties.get('dob', "")) is not str:
            raise TypeError("'dob' must be a string.")
        else:
            try:
                dobObj = dateparser.parse(properties.get('dob')).date()
            except dateparser.ParserError as error:
                raise TypeError("'dob' must be a valid date.")
        if type(properties.get('friends', [])) is not list:
            raise TypeError("'dob' must be an array of strings.")
        
        # Insert row and create user profile:
        data, count = sb.table('user_profiles').insert({
            "id": self.id,
            "username": self.username,
            "first_name": properties.get('first_name') or self.first_name,
            "last_name": properties.get('last_name') or self.last_name,
            "dob": dobObj.isoformat() or self.dob.isoformat(),
            "friends": self.friends
        }).execute()
        
        if data is None:
            raise SupabaseException("Error creating profile.")
        else:
            self.getProfile()
        
    def updateProfile(self, properties:dict={}) -> None:
        sb = get_sb()
        
        # Validation and typecasting:
        if type(properties.get('first_name', "")) is not str:
            raise TypeError("'first_name' must be a string.")
        if type(properties.get('last_name', "")) is not str:
            raise TypeError("'last_name' must be a string.")
        if type(properties.get('dob', "")) is not str:
            raise TypeError("'dob' must be a string.")
        else:
            try:
                dobObj = dateparser.parse(properties.get('dob')).date()
            except dateparser.ParserError as error:
                raise TypeError("'dob' must be a valid date.")
        if type(properties.get('friends', [])) is not list:
            raise TypeError("'dob' must be an array of strings.")
        
        # Update user profile database:
        data = sb.table('user_profiles').update({
            "first_name": properties.get('first_name') or self.first_name,
            "last_name": properties.get('last_name') or self.last_name,
            "dob": dobObj.isoformat() or self.dob,
            "friends": properties.get('friends') or self.friends
        }).eq('id', self.id).execute()
        
        if data is None and properties:
            raise SupabaseException("Error updating profile.")
        else:
            self.getProfile()
            
    def getSwipes(self) -> None:
        sb = get_sb()
        res = sb.table('recommendations').select("left_swipes,right_swipes").eq("id", self.id).execute()
        # If user's swipe data exists, save it to local instance:
        if len(res.data) == 1:
            self.left_swipes = res.data[0].get("left_swipes", [])
            self.right_swipes = res.data[0].get("right_swipes", [])
            
    def swipe(self, restaurantObj:Restaurant, direction:str) -> None:
        # Validation:
        if restaurantObj.id is None:
            raise ServerSideError("Restaurant does not exist.")
        direction = direction.lower().strip()
        if direction not in ["left", "right"]:
            raise ClientSideError("Invalid swipe direction. Must be 'LEFT' or 'RIGHT'")
        
        # Store data in Supabase
        sb = get_sb()
        self.getSwipes()
        if direction == "left" and restaurantObj.id not in self.left_swipes:
            proposed = self.left_swipes.copy()
            proposed.append(restaurantObj.id)
            res = sb.table('recommendations').upsert({
                "id": self.id,
                f"{direction}_swipes": proposed
            }).execute()
            self.left_swipes = proposed
        elif direction == "right" and restaurantObj.id not in self.right_swipes:
            proposed = self.right_swipes.copy()
            proposed.append(restaurantObj.id)
            res = sb.table('recommendations').upsert({
                "id": self.id,
                f"{direction}_swipes": proposed
            }).execute()
            self.right_swipes = proposed
        
        # res = sb.table('recommendations').select(f'{direction}_swipes').eq('id', self.id).execute()
        # # Row doesn't exist or just direction of swipes list doesn't exist:
        # if len(res.data) == 0 or res.data[0][f"{direction}_swipes"] is None:
        #     newData = [restaurantObj.id]
        # # Add restaurant ID to array if it is not already there:
        # elif restaurantObj.id not in res.data[0][f"{direction}_swipes"]:
        #     newData = res.data[0][f"{direction}_swipes"].copy()
        #     newData.append(restaurantObj.id)
        # # Otherwise, no updates
        # else:
        #     newData = None
        # # Update if we have new data:
        # if newData is not None:
        #     res = sb.table('recommendations').upsert({
        #         "id": self.id,
        #         f"{direction}_swipes": newData
        #     }).execute()
        #     print(res.data)
        
    def __repr__(self):
        return json.dumps(self._dict, indent=2)

    
class SupabaseException(Exception):
    """Raised when there is an error in a call to the Supabase API."""
    pass

class ClientSideError(Exception):
    """Raised when there is an expected client side error."""
    pass

class ServerSideError(Exception):
    """Raised when there is an expected server side error."""
    pass

class Redirect(Exception):
    """Raised when there is an exception that can be solved with a redirect."""
    def __init__(self, message:str, uri:str):
        self.uri = uri
        super(Redirect, self).__init__(message)

class EmailUnverified(Exception):
    """Raised when user account is created but email is not verified."""
    pass