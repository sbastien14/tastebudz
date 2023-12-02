import pytest, logging, uuid, random, re, datetime
from time import sleep
from tastebudz.models import Restaurant, User
from tastebudz.sb import get_sb
from flask import g
from starlette.testclient import TestClient
from faker import Faker

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
        

##################################### RESTAURANT CLASS #####################################
class TestRestaurantClass:
    # Define parameters for test functions:
    @classmethod
    def initParams(cls, faker):
        cls.params = {
            "test_recommendation_from_no_data": [{"user": None, "password": None}]
        }
        # Dynamically create some temporary users:
        # for i in range(1):
        #     profile = faker.simple_profile()
        #     password = "".join(faker.words().append(str(random.randrange(0,1000))).append(random.choice(["!", "$", "#", "*"])))
        #     sb = get_sb()
        #     res = sb.auth.sign_up({
        #         "email": profile["mail"],
        #         "password": password,
        #         "options": {
        #             "data": {
        #                 "username": profile["username"],
        #                 "role": random.randint(0,1)
        #             }
        #         }
        #     })
        #     cls.params["test_recommendation_from_no_data"].append({
        #         "user": User(res),
        #         "password": password
        #     })
        
        # Dynamically generate some restaurant IDs:
        for i in range(1):
            ...
            # search = yelpClient.searchBusiness(location="Syracuse, NY")
            # id = random.choice(search["businesses"])["id"]
            # cls.params["test_instantiation_valid_id"].append({"id": id})
        
    
    # def test_instantiation_valid_id(self, id:str):
    #     # search = yelpClient.searchBusiness(location="Syracuse, NY")
    #     # id = random.choice(search["businesses"])["id"]
    #     print(id)
    #     assert id is None
    
    @pytest.mark.skip
    def test_recommendation_from_no_data(self, client, flaskApp, auth, user:User, password:str):
        with flaskApp.app_context():
            with client:
                auth.login_with_password(user.email, password)
                
                response = client.get("/restaurant/recommendation")
                assert response.status_code == 200
                
                auth.logout()