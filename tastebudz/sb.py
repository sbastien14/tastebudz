import click, logging
from supabase import create_client, Client
# from supabase.client import ClientOptions
from flask import current_app, g, Flask

# Retrieve current instance from session or create new instance:
def get_sb() -> Client:
    if 'sb' not in g:
        g.sb = create_client(
            current_app.config["SUPABASE_URL"], 
            current_app.config["SUPABASE_SERVICE_ROLE_KEY"]
            # options=ClientOptions(
            #     postgrest_client_timeout=10
            # )
        )
        logging.getLogger().info("[SUPABASE] Created instance.")
    else:
        logging.getLogger().info("[SUPABASE] Got current instance.")
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
    try:
        sb.auth.close()
        # sb.realtime.close()
        # if sb._postgrest is not None: sb._postgrest.close()
    except Exception as error:
        logging.getLogger().error(f"Failed to close Supabase instance; {type(error)}: {str(error)}")
    if sb is not None:
        pass
    logging.getLogger().info("[SUPABASE] Closed instance.")

# Use this file by calling init_app on the instance:
def init_app(app:Flask):
    app.teardown_appcontext(close_sb)
    app.cli.add_command(get_sb_command)