import pytest, logging, random
from tastebudz import create_app
from tastebudz.models import User
from tastebudz.yelp_api import YelpClient
from supabase import create_client
from config import Config
from flask import g

@pytest.fixture()
# Creates and returns Connexion App which wraps Flask App
def app():
    app = create_app()
    app.app.config.update({
        "TESTING": True,
        "SERVER": "http://127.0.0.1:5000"
    })
    # Setup any other resources here.
    yield app
    # Teardown any other resources here.
    

@pytest.fixture()
# Returns Flask App
def flaskApp(app):
    return app.app
    
@pytest.fixture()
def supabaseClient():
    sb = create_client(
        Config.SUPABASE_URL,
        Config.SUPABASE_SERVICE_ROLE_KEY
    )
    return sb

@pytest.fixture()
def yelpClient():
    y = YelpClient(Config.YELP_API_KEY)
    return y

# Creates a temporary user for testing and deletes the user when done.
@pytest.fixture()
def temporaryUser(flaskApp, faker):
    profile = faker.simple_profile()
    with flaskApp.app_context():
        # Create user account:
        password = "".join(faker.words().append(str(random.randrange(0,1000))).append(random.choice(["!", "$", "#", "*"])))
        res = g.sb.auth.sign_up({
            "email": profile["mail"],
            "password": password,
            "options": {
                "data": {
                    "username": profile["username"],
                    "role": random.randint(0,1)
                }
            }
        })
        user = User(res)
        # Create user profile using pre-built class:
        user.createProfile({
            "first_name": profile["name"].split()[0],
            "last_name": profile["name"].split()[1],
            "dob": profile["birthdate"].isoformat()
        })
        
        yield (user, password)
        
        # Delete user account:
        res = g.sb.auth.admin.delete_user(user.id)     

    
@pytest.fixture()
# Returns Connexion test client (Starlette)
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client
        self._valid_accounts = [
            ("jnmosca+testuser1@syr.edu", "P@ssw0rd!"),
            ("jnmosca+testuser2@syr.edu", "P@ssw0rd!"),
            ("jnmosca+testuser3@syr.edu", "P@ssw0rd!"),
            ("jnmosca+testy@syr.edu", "SuperSecretPassword!")
        ]
        
    def login_with_password(self, email:str="jnmosca+testuser1@syr.edu", password:str="P@ssw0rd!"):
        res = self._client.get(
            "/auth/user/login",
            auth=(email, password)
        )
        self._client.cookies = res.cookies
        # logging.getLogger().info(f"Cookies: {res.cookies}")
        return res
    
    def logout(self):
        res = self._client.get(f"/auth/user/logout")
        self._client.cookies.clear()
        logging.getLogger().info(f"Cookies: {self._client.cookies}")
        return res
    
    def temporary_user(self, faker):
        # Create user account:
        profile = faker.simple_profile()
        password = "".join(faker.words().append(str(random.randrange(0,1000))).append(random.choice(["!", "$", "#", "*"])))
        res = g.sb.auth.sign_up({
            "email": profile["mail"],
            "password": password,
            "options": {
                "data": {
                    "username": profile["username"],
                    "role": random.randint(0,1)
                }
            }
        })
        user = User(res)
        # Create user profile using pre-built class:
        user.createProfile({
            "first_name": profile["name"].split()[0],
            "last_name": profile["name"].split()[1],
            "dob": profile["birthdate"].isoformat()
        })
    
@pytest.fixture()
def auth(client):
    return AuthActions(client)


@pytest.fixture()
def vcr_config():
    return {
        "ignore_localhost": False,
        "allowed_hosts": ["localhost", "*.supabase.co*"],
        "record_mode": "rewrite"
    }