import logging
from functools import wraps
from flask import (
    Blueprint, flash, g, redirect, make_response, request, url_for, session
)
from gotrue.errors import AuthApiError
from pydantic_core._pydantic_core import ValidationError
from postgrest.exceptions import APIError
from tastebudz.sb import get_sb
from tastebudz.models import User
from connexion import context as ccontext

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return { "message": "You must be logged in to do this." }, 401          
        return view(**kwargs)
    return wrapped_view
            
# @bp.route('/user', methods=['POST'])
def register(body):
    requestBody = body
    email = request.authorization.username
    password = request.authorization.password
    username = requestBody.get('username')
    role = requestBody.get('role', 0)
    
    # Default to an unknown server error:
    body = {"message": "An unknown error has occurred."}
    statusCode = 500
    sb = get_sb()
    
    if email and password:
        try:
            # Create user account:
            res = sb.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username,
                        "role": role
                    }
                }
            })
            print(res)
        except AuthApiError as error:
            body["message"] = f"{type(error)}: {str(error)}"
            statusCode = 502
            logging.getLogger().error(f"[AUTH/REGISTER] Upstream API raised {type(error)}: {str(error)}")
        except Exception as error:
            body["message"] = f"{type(error)}: {str(error)}"
            statusCode = 500
            logging.getLogger().error(f"[AUTH/REGISTER] Internal server raised {type(error)}: {str(error)}")
        else:
            # Awaiting email verification:
            if res.session is None:
                unverifiedUser = User(res.user)
                body['message'] = 'Account created; awaiting email verification.'
                body['user'] = unverifiedUser
                statusCode = 202
                logging.getLogger().warn(f"[AUTH/REGISTER] Account created for {unverifiedUser.username} pending email verification at {unverifiedUser.email}")
            # User account created successfully:
            else:
                g.user = User(res.user)
                
                body['message'] = 'Account created successfully.'
                body['user'] = g.user
                statusCode = 201
                logging.getLogger().warn(f"[AUTH/REGISTER] Account created for {g.user.username}")
    elif not email:
        body = {"message": "Email is required but was not provided."}
        statusCode = 400
        logging.getLogger().error("[AUTH/REGISTER] Email is required but was not provided (provide via HTTP basic auth).")
    elif not password:
        body = {"message": "Password is required but was not provided."}
        statusCode = 400
        logging.getLogger().error("[AUTH/REGISTER] Password is required but was not provided (provide via HTTP basic auth).")
    else:
        # Did not receive valid form data:
        body = {"message": "Invalid form data submitted."}
        statusCode = 400
        logging.getLogger().error(f"[AUTH/REGISTER] Invalid form data:\n\tEmail: {email}\n\t{'*'*5 if password is not None else "None"}\n\tUsername: {username}\n\tRole: {role}")
                
    return body, statusCode

@login_required
def deleteUser(username:str):
    if username != g.user.username:
        body = {"message": f"{g.user.username or g.user.email} is currently logged-in; you must log in as {username} to delete this account."}
        statusCode = 400
        logging.getLogger().error(f"[AUTH/DELETE] Could not delete; supplied username ({g.user.username}) does not match logged-in account.")
    else:
        sb = get_sb()
        try:
            res = sb.auth.admin.delete_user(g.user.id)
        except AuthApiError as error:
            body = {"message": f"{type(error)}: {str(error)}"}
            statusCode = 502
            logging.getLogger().error(f"[AUTH/DELETE] Upstream API raised {type(error)}: {str(error)}")
        except Exception as error:
            body = {"message": f"{type(error)}: {str(error)}"}
            statusCode = 500
            logging.getLogger().error(f"[AUTH/DELETE] Internal server raised {type(error)}: {str(error)}")
        else:
            body = {
                "message": f"Successfully deleted {g.user.username or g.user.email}.",
                "user": g.user
            }
            statusCode = 200
            logging.getLogger().info(f"[AUTH/DELETE] Permanently deleted {g.user.username}")
            # Cleanup logged-in:
            logout()
    
    return body, statusCode
            

# @bp.route('/user/login', methods=['GET'])
def login(oauth_provider:str=None, access_token:str=None, refresh_token:str=None):
    sb = get_sb()
    
    # Default to an unknown server error:
    body = { "message": "An unknown error has occurred." }
    statusCode = 500
    headers = {}
    
    if request.authorization is not None:
        # Get email and password from HTTP basic auth:
        email = request.authorization.username
        password = request.authorization.password
        logging.getLogger().info(f"[AUTH/LOGIN] Received login with password for {email}.")
        if email is None or email == "":
            logging.getLogger().error("[AUTH/LOGIN] Email is required but not provided.")
            body["message"] = "Email is required but was not provided."
            statusCode = 400
        elif password is None or password == "":
            logging.getLogger().error("[AUTH/LOGIN] Password is required but was not provided.")
            body["message"] = "Password is required but was not provided."
            statusCode = 400
        else:
            try:
                res = sb.auth.sign_in_with_password({"email": email, "password": password})
            # The Supabase API returned an error:
            except AuthApiError as error:
                body["message"] = f"{type(error)}: {str(error)}"
                if "Invalid" in str(error):
                    statusCode = 401
                else:
                    statusCode = 502
            # There was another error (likely our fault):
            except Exception as error:
                # Use default server error:
                body["message"] = f"{type(error)}: {str(error)}"
                statusCode = 500
            # No errors, we are signed in:
            else:
                g.user = User(res.user)
                logging.getLogger().info("[AUTH/LOGIN] Successfully created user object.")
                # body = {
                #     "message": f"Successfully signed in {g.user.username or g.user.email}.",
                #     "user": g.user
                # }
                # statusCode = 200
    # OAuth process has returned from provider with access token:
    elif access_token and refresh_token:
        try:
            res = sb.auth.set_session(access_token, refresh_token)
        # Supabase API returned an error:
        except AuthApiError as error:
            body['message'] = str(error)
            statusCode = 502
        # There was another error (likely our fault):
        except Exception as error:
            # Use default server error:
            body["message"] = str(error)
            statusCode = 500
        # No errors, we're signed in!
        else:
            g.user = User(res.user)
            logging.getLogger().info("[AUTH/LOGIN] Successfully creates user object.")
    # Return redirect URL for OAuth with requested provider:
    elif oauth_provider is not None:
        try:
            res = sb.auth.sign_in_with_oauth({
                "provider": oauth_provider,
                "options": {
                    "redirect_to": "http://localhost:5000/auth/user/login"
                }
            })
        # Supabase API returned an error:
        except AuthApiError as error:
            body["message"] = f"{type(error)}: {str(error)}"
            statusCode = 502
        except ValidationError as error:
            body["message"] = f"{type(error)}: {str(error)}"
            statusCode = 400
        # There was another error (likely our fault):
        except Exception as error:
            # Use default server error:
            body["message"] = f"{type(error)}: {str(error)}"
            statusCode = 500
        else:
            body["message"] = f"Sign in with {res.provider.capitalize()}"
            statusCode = 303
            headers["Location"] = res.url
    else:
        body = { "message": "Unknown client error; please make sure the required parameters were provided." }
        statusCode = 400
        
    #TODO: if login was successful, try generating shortstack'
    #      of recommendations and add to session.
    # If we have been authenticated, finish logging in:
    if g.get('user') is not None:
        # print(res)
        body = {
            "message": f"Successfully signed in {g.user.username or g.user.email}.",
            "user": g.user
        }
        statusCode = 200
    response = make_response(body, statusCode, headers)
    # response.set_cookie
          
    return response

# @bp.route('/logout')
@login_required
def logout():
    sb = get_sb()
    
    # Default to an unknown server error:
    body = { "message": "An unknown error has occurred." }
    statusCode = 500
    
    try:
        res = sb.auth.sign_out()
        #TODO: clear shortstack of recs from session
    except AuthApiError as error:
        body["message"] = str(error)
        statusCode = 502
    except Exception as error:
        body["message"] = str(error)
        statusCode = 500
    else:
        body = {
            "message": f"Successfully logged out {g.user.username or g.user.email}.",
            "user": g.user
        }
        statusCode = 200
        
    return body, statusCode

@login_required
def getUserProfile(username:str):
    sb = get_sb()
    
    try:
        g.user.getProfile()
    except Exception as error:
        body = { "message": f"{type(error)}: {str(error)}" }
        statusCode = 500
    else:
        body = {
            "message": f"Successfully retrieved user profile for {g.user.username or g.user.email}.",
            "user": g.user
        }
        statusCode = 200
        
    return body, statusCode

@login_required
def createUserProfile(username:str, body):
    sb = get_sb()
    requestBody = body
    
    # Only attempt to create profile for user that is logged-in:
    if username != g.user.username:
        body = { "message": "Can only create profile for currently logged-in user." }
        statusCode = 400
    else:
        try:
            g.user.createProfile(requestBody)
        except APIError as error:
            logging.getLogger().error(f"User profile already exists; {type(error)}: {str(error)}")
            if error.code == "23505":
                body = { "message":  f"Failed; user profile for {g.user.username or g.user.email} already exists." }
                statusCode = 400
        except Exception as error:
            body = { "message": f"{type(error)}: {str(error)}" }
            statusCode = 500
        else:
            body = {
                "message": f"Created user profile for {g.user.username or g.user.email}.",
                "user": g.user
            }
            statusCode = 201
        
    return body, statusCode

@login_required
def updateUserProfile(username:str, body):
    sb = get_sb()
    requestBody = body
    print(requestBody)
    
    try:
        g.user.updateProfile(requestBody)
        # g.user.updateProfile(requestBody)
    except Exception as error:
        body = { "message": f"{type(error)}: {str(error)}" }
        statusCode = 500
    else:
        body = {
            "message": f"Successfully updated user profile for {g.user.username or g.user.email}",
            "user": g.user
        }
        statusCode = 200
        
    return body, statusCode
    

@bp.before_app_request
def load_logged_in_user():
    sb = get_sb()
    res = sb.auth.get_user()
    #TODO: also call some function to check session for recs \
        # and populate it if we're getting low.
    if res is not None:
        g.user = User(res.user)
        logging.getLogger().info(f"[AUTH/REQUEST] Retrieved logged-in user {g.user.username}")
    else:
        g.user = None
        logging.getLogger().warn(f"[AUTH/REQUEST] User not logged-in.")
    