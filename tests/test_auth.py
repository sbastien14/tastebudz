import pytest, logging
from flask import g

@pytest.mark.skip
@pytest.mark.vcr
def test_logout_with_password(client, flaskApp, auth):
    login_resp = auth.login_with_password()
    logging.getLogger().info(login_resp.text)
    logging.getLogger().info(login_resp.cookies)
    with client:
        response = auth.logout()
        logging.getLogger().info(response.text)
        logging.getLogger().info(response.cookies)
        assert response.status_code == 100
    with flaskApp.app_context():
        with client:
            client.get("/")
            assert "user" not in g or g.user == None
            


@pytest.mark.parametrize(('email', 'password', 'statusCode'),(
    ("jnmosca+testuser1@syr.edu", "P@ssw0rd!", 200),
    ("jnmosca+testuser1@syr.edu", "P@ssw0rd", 401),
    ("", "P@ssw0rd", 400),
    ("jnmosca+testuser1@syr.edu", "", 400),
    ("jnmosca+testuser2@syr.edu", "P@ssw0rd!", 200),
    ("jnmosca+testuser2@syr.edu", "N0tMyP@55w0rd!", 401),
    ("jnmosca+testuser3@syr.edu", "P@ssw0rd!", 200),
    ("jnmosca+testuser3@syr.edu", "4LS0N0TM1N3$", 401),
    ("jnmosca+testuserA@syr.edu", "Password1234", 401)
))
def test_login_with_password(client, flaskApp, auth, email:str, password:str, statusCode:int):    
    with flaskApp.app_context():
        with client:
            # response = client.get("/auth/user/login", auth=(email, password))
            response = auth.login_with_password(email, password)
            logging.getLogger().warning(response.text)
            assert response.status_code == statusCode
            if statusCode == 200:
                assert g.user is not None
                assert g.user.email == email
                auth.logout()
            

@pytest.mark.parametrize(('oauth_provider', 'statusCode'), (
    ("google", 303),
    ("", 400),
    ("notAProvider", 400),
    ("google", 303)
))
@pytest.mark.vcr()
def test_get_oauth_url(client, oauth_provider:str, statusCode:str):
    testQuery = {
        "oauth_provider": oauth_provider
    }
    with client:
        response = client.get("/auth/user/login", params=testQuery, follow_redirects=False)
        logging.getLogger().warning(response.text)
        assert response.status_code == statusCode
        if statusCode == 303:
            logging.getLogger().warning(response.headers)
            assert "Location" in response.headers
            

# @pytest.mark.parametrize(('access_token', 'refresh_token', 'statusCode'), (
#     ("")
# ))
# def test_login_with_oauth(client, access_token:str, refresh_token:str, statusCode:int):
#     testQuery = {
#         "access_token": access_token,
#         "refresh_token": refresh_token
#     }
#     with client:
#         response = client.get("/auth/user/login", params=testQuery)
#         logging.getLogger().warning(response.data.decode("utf-8"))
#         assert response.status_code == statusCode
#         if statusCode == 200:
#             assert g.user is not None