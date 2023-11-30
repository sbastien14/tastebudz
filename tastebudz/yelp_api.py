import click, requests
from yelp.client import Client
from flask import current_app, g, Flask

# Retrieve current instance from session or create new instance:
def get_yelp() -> Client:
    if 'yelp' not in g:
        g.yelp = YelpClient(current_app.config['YELP_API_KEY'])
    return g.yelp

# Flask command to wrap get_yelp():
@click.command('get-yelp')
def get_yelp_command():
    """Initialize connection to Yelp API"""
    get_yelp()
    click.echo("Connected to Yelp API.")

# Close instance (no need to do anything for this module):
def close_yelp(e=None) -> None:
    yelp_api = g.pop('yelp', None)
    if yelp_api is not None:
        pass
    
# Use this file by calling init_app on the instance:
def init_app(app:Flask):
    app.teardown_appcontext(close_yelp)
    app.cli.add_command(get_yelp_command)
    
class YelpClient:
    def __init__(self, api_key:str):
        self.api_key:str = api_key
        
        headers = {
            "authorization": f"Bearer {self.api_key}",
            "accept": "application/json"
        }
        self._session = requests.Session()
        self._session.headers = headers
    
    def getBusiness(self, id:str):
        query = {
            "device_platform": "mobile-generic"
        }
        url = f"https://api.yelp.com/v3/businesses/{id}"
        response = self._session.get(url, params=query)
        response.raise_for_status()
        return response.json()
    
    def searchBusiness(self, location:str=None, latitude:float=None, longitude:float=None,
                       term:str=None, radius:int=None, categories:list=None, locale:str=None,
                       price:list=None, open_now:bool=None, open_at:int=None, attributes:list=None,
                       sort_by:str=None, device_platform:str="mobile-generic", reservation_date:str=None,
                       reservation_time:str=None, reservation_covers:int=None,
                       matches_party_size_param:bool=None, limit:int=20, offset:int=None):
        args = locals()
        # Validation:
        if location is None and (latitude is None and longitude is None):
            raise Exception("You must specify location or a latitude and longitude.")
        
        # Send request:
        query = dict([(item, args[item]) for item in args if args[item] is not None and item != "self"])
        url = "https://api.yelp.com/v3/businesses/search"
        response = self._session.get(url, params=query)
        response.raise_for_status()
        return response.json()