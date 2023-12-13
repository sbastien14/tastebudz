import pytest, logging, uuid, random, re, datetime
from time import sleep
from tastebudz.models import User
from flask import g
from starlette.testclient import TestClient
from faker import Faker
from gotrue import User as SupabaseUser

################################### PARAMETER GENERATION ###################################
def pytest_generate_tests(metafunc):
    # Generate parameters at collection time if class has the initParams()
    # classmethod:
    if hasattr(metafunc.cls, "initParams"):
        faker = Faker()
        metafunc.cls.initParams(faker)
        logging.getLogger().info(f"[PYTEST] {metafunc.function.__name__} - Dynamically generated parameters.")
    # Parametrize pytest test cases with statically defined parameters
    # defined as "params" class attribute:
    if hasattr(metafunc.cls, "params"):
        funcarglist = metafunc.cls.params[metafunc.function.__name__]
        argnames = sorted(funcarglist[0])
        metafunc.parametrize(
            argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
        )
        logging.getLogger().info(f"[PYTEST] {metafunc.function.__name__} - Parametrized test case.")


######################################## USER CLASS ########################################
class TestUserClass:
    # Define parameters for test functions:
    @classmethod
    def initParams(cls, faker):
        cls.params = {}
        # Create some instances of supabase User:
        sbUsers = []
        for i in range(10):
            sbUsers.append(cls._create_supabase_user(faker))
        cls.params["test_account_instantiation"] = [{"supabaseUser": usr} for usr in sbUsers]
        # Pull valid user accounts from fixture:
        cls.params["test_profile_instantiation"] = [
            # {"username": "jnmosca+testuser1@syr.edu", "password": "P@ssw0rd!"},
            # {"username": "jnmosca+testuser2@syr.edu", "password": "P@ssw0rd!"},
            {"username": "jnmosca+testuser3@syr.edu", "password": "P@ssw0rd!"},
            {"username": "jnmosca+testuser4@syr.edu", "password": "SuperSecretPassword!"},
            # {"username": "jnmosca+testy@syr.edu", "password": "SuperSecretPassword!"},
        ]
    
    @classmethod
    def _create_supabase_user(cls, faker) -> SupabaseUser:
        profile:dict = faker.simple_profile()
        usr = SupabaseUser(
            id=str(uuid.uuid4()),
            app_metadata={},
            user_metadata={
                "role": random.randrange(0, 2),
                "username": profile["username"]
            },
            aud="authenticated",
            confirmation_sent_at=faker.date_time_between(),
            email=profile["mail"],
            phone=faker.phone_number(),
            created_at=faker.date_time_between(),
            confirmed_at=faker.date_time_between(),
            last_sign_in_at=faker.date_time_between("-1y", "now"),
            role="authenticated"
        )
        return usr
    
    
    def test_account_instantiation(self, supabaseUser:SupabaseUser):
        user = User(supabaseUser)
        assert user is not None
        assert user._dict is not None
        userDictKeys = ["id", "username", "email", "phone", "role", "first_name", "last_name", 'dob', "friends"]
        assert sorted(userDictKeys) == sorted(user._dict.keys())
        assert uuid.UUID(user.id)
        assert re.match("^[\w_.-]+@[\w_.+-]+\.[\w]{2,4}$", user.email) is not None
        assert re.match("^[\+]?[0-9]{0,3}[-\s\.]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}(?:x[0-9]{1,5})?$", user.phone) is not None or user.phone == ""
        assert user.username is not None
        assert user.role in [0, 1]
        
    
    def test_profile_instantiation(self, auth, flaskApp, username:str, password:str):
        with flaskApp.app_context():
            auth.login_with_password(username, password)
            assert g.user is not None
            assert g.user.first_name != ""
            assert g.user.last_name != ""
            assert type(g.user.dob) == datetime.date


###################################### USER COMPONENT ######################################

# @pytest.mark.parametrize(("username", "first_name", "last_name", "dob", "statusCode"), (
#     ("TestUser3", "John", "Sims", "01-01-1971", 400),
#     # ("TestUser3", None, "Sims", "01-01-1971", 200),
#     # ("TestUser3", "John", None, "01-01-1971", 200),
#     # ("TestUser3", "John", "", "01-01-1971", 200),
#     # ("TestUser3", "John", "Sims", "03-31-2000", 200),
#     # ("", "John", "Sims", "01-01-1971", 404),
#     # (None, "John", "Sims", "01-01-1971", 400),
# ))
class TestUserComponent:
    # Define parameters for test functions:
    @classmethod
    def initParams(cls, faker):
        # Initialize static parameters:
        cls.params = {
            "test_create_user_profile": [
                {"username": "TestUser3", "first_name": "John", "last_name": "Sims", "dob": "01-01-1971", "statusCode": 400}
            ],
            "test_create_account_with_password": [],
            "test_delete_user_account": [{"statusCode": 200}]
        }
        # Initialize dynamic parameters:
        for i in range(1):
            usr = cls._createRandomUser(faker)
            cls.params["test_create_account_with_password"].append({
                "username": usr.username,
                "email": usr.email,
                "password": cls._createRandomPassword(faker),
                "role": usr.role,
                "statusCode": 202  # May be 201 if email verification is disabled.
            })
        # for i in range(1):
        #     usr = cls._createRandomUser(faker)
        #     cls.params["test_delete_user_account"].append({
        #         "username": usr.username,
        #         "email": usr.email,
        #         "password": cls._createRandomPassword(faker),
        #         "role": usr.role,
        #         "statusCode": 200
        #     })
        

    
    
    @staticmethod
    def _createRandomUser(faker):
        profile = faker.simple_profile()
        userData = {
            "id": uuid.uuid4(),
            "username": profile["username"],
            "email": profile["mail"],
            "phone": faker.phone_number(),
            "role": random.randint(0,1),
            "first_name": profile["name"].split()[0],
            "last_name": profile["name"].split()[1],
            "dob": profile["birthdate"].isoformat(),
            "friends": []
        }
        return User(userData)
    
    @staticmethod
    def _createRandomPassword(faker):
        password = "".join(faker.words()) + str(random.randrange(0,1000)) + str(random.choice(["!", "$", "#", "*"]))
        return password
        
    
    @pytest.mark.vcr
    def test_create_user_profile(self, client:TestClient, flaskApp, auth,
                                username:str, first_name:str,
                                last_name:str, dob:str,
                                statusCode:int):
        auth.login_with_password("jnmosca+testuser3@syr.edu", "P@ssw0rd!")
        with flaskApp.app_context():
            with client:
                testBody = {}
                if first_name: testBody["first_name"] = first_name
                if last_name: testBody["last_name"] = last_name
                if dob: testBody["dob"] = dob
                resp = client.post(f"/auth/user/{username}", json=testBody)
                logging.getLogger().info(resp.text)
                
                assert resp.status_code == statusCode
                # assert resp is None
                auth.logout()
            logging.getLogger().error(client.cookies)
            
    
    # NOTE: these API calls are rate-limited, so limit testing.
    def test_create_account_with_password(self, client:TestClient, flaskApp, supabaseClient, username:str,
                                          password:str, role:int, email:str, statusCode:int):
        with flaskApp.app_context():
            with client:
                testBody = {
                    "username": username,
                    "role": role
                }
                testCreds = (email, password)
                resp = client.post(f"/auth/user", json=testBody, auth=testCreds)
                assert resp.status_code == statusCode
                
                # Verify successfully created user:
                if statusCode in [201, 202]:
                    assert "user" in resp.json()
                    assert resp.json()["user"]["username"] == username
                    assert resp.json()["user"]["email"] == email
                    assert resp.json()["user"]["role"] == role
                
                # Delete created user:
                sleep(10)
                if statusCode in [201, 202]:
                    supabaseClient.auth.admin.delete_user(resp.json()["user"]["id"])
                    

    # @pytest.mark.skip
    # NOTE: these API calls are rate-limited, so limit testing.
    def test_delete_user_account(self, client, flaskApp, auth, supabaseClient, faker, statusCode:int):
        # Create random user account:
        profile = faker.simple_profile()
        password = "".join(faker.words())
        # password = "".join(faker.words().append(str(random.randrange(0,1000))).append(random.choice(["!", "$", "#", "*"])))
        res = supabaseClient.auth.sign_up({
            "email": profile["mail"],
            "password": password,
            "options": {
                "data": {
                    "username": profile["username"],
                    "role": random.randint(0,1)
                }
            }
        })
        
        sleep(5)
        
        with flaskApp.app_context():
            with client:
                auth.login_with_password(profile["mail"], password)
                sleep(2)
                
                resp = client.delete(f"/auth/user/{profile["username"]}")
                assert resp.status_code == statusCode
                sleep(2)
                
                auth.logout()