import click, googlemaps
from flask import current_app, g, Flask

# Retrieve current instance from session or create new instance:
def get_gmaps() -> googlemaps.Client:
    if 'gmaps' not in g:
        g.gmaps = googlemaps.Client(key=current_app.config["GOOGLE_MAPS_API_KEY"])
    return g.gmaps

# Flask command to wrap get_gmaps():
@click.command('get-gmaps')
def get_gmaps_command():
    """Initialize connection to Google Maps API"""
    get_gmaps()
    click.echo("Connected to Google Maps API.")

# Close instance (no need to do anything for this module):
def close_gmaps(e=None) -> None:
    gmaps = g.pop('gmaps', None)
    if gmaps is not None:
        pass
    
# Use this file by calling init_app on the instance:
def init_app(app:Flask):
    app.teardown_appcontext(close_gmaps)
    app.cli.add_command(get_gmaps_command)