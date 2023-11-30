import pytest, logging, uuid, random, re, datetime
from time import sleep
from tastebudz.models import Restaurant
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
            "test_instantiation_valid_id": [{"id": "bbq"}]
        }
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