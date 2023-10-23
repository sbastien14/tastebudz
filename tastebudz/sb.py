import click
from supabase import create_client, Client
from flask import current_app, g, Flask

# Retrieve current instance from session or create new instance:
def get_sb() -> Client:
    if 'sb' not in g:
        g.sb = create_client(current_app.config["SUPABASE_URL"], current_app.config["SUPABASE_KEY"])
    return g.sb

# Flask command that wraps get_gmaps():
@click.command('get-sb')
def get_sb_command():
    """Initialize connection to Supabase"""
    get_sb()
    click.echo('Initialized connection to Supabase.')

# Close instance (no need to do anything for this module):
def close_sb(e=None) -> None:
    sb = g.pop('sb', None)
    if sb is not None:
        pass

# Use this file by calling init_app on the instance:
def init_app(app:Flask):
    app.teardown_appcontext(close_sb)
    app.cli.add_command(get_sb_command)