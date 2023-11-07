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
    
    def getBusiness(self, id:str):
        url = f"https://api.yelp.com/v3/businesses/{id}"
        query = {
            "device_platform": "mobile-generic"
        }
        headers = {
            "authorization": f"Bearer {self.api_key}",
            "accept": "application/json"
        }
        response = requests.get(url, headers=headers, params=query)
        response.raise_for_status()
        return response.json()