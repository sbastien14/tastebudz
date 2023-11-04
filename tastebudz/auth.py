from functools import wraps
from flask import (
    Blueprint, flash, g, redirect, make_response, request, url_for, session
)
from gotrue.errors import AuthApiError, AuthSessionMissingError
from tastebudz.sb import get_sb
from tastebudz.models import User
import json, time
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
            body["message"] = str(error)
            statusCode = 502
        except Exception as error:
            body["message"] = str(error)
            statusCode = 500
        else:
            # Awaiting email verification:
            if res.session is None:
                body['message'] = 'Account created; awaiting email verification.'
                body['user'] = User(res.user)
                statusCode = 202
            # User account created successfully:
            else:
                g.user = User(res.user)
                
                body['message'] = 'Account created successfully.'
                body['user'] = g.user
                statusCode = 201
    elif not email:
        body = {"message": "Email is required but was not provided."}
        statusCode = 400
    elif not password:
        body = {"message": "Password is required but was not provided."}
        statusCode = 400
    else:
        # Did not receive valid form data:
        body = {"message": "Invalid form data submitted."}
        statusCode = 400
                
    return body, statusCode
            

# @bp.route('/user/login', methods=['GET'])
def login(oauth_provider:str=None, access_token:str=None, refresh_token:str=None, **kwargs):
    sb = get_sb()
    
    # Default to an unknown server error:
    body = { "message": "An unknown error has occurred." }
    statusCode = 500
    headers = {}
    
    if request.authorization is not None:
        # Get email and password from HTTP basic auth:
        email = request.authorization.username
        password = request.authorization.password
        if email is None:
            body["message"] = "Email is required but was not provided."
            statusCode = 400
        elif password is None:
            body["message"] = "Password is required but was not provided."
            statusCode = 400
        else:
            try:
                res = sb.auth.sign_in_with_password({"email": email, "password": password})
            # The Supabase API returned an error:
            except AuthApiError as error:
                body["message"] = str(error)
                statusCode = 502
            # There was another error (likely our fault):
            except Exception as error:
                # Use default server error:
                body["message"] = str(error)
                statusCode = 500
            # No errors, we are signed in:
            else:
                g.user = User(res.user)

                body = {
                    "message": f"Successfully signed in {g.user.username or g.user.email}.",
                    "user": g.user
                }
                statusCode = 200
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

            body = {
                "message": f"Successfully signed in {g.user.username or g.user.email}.",
                "user": g.user
            }
            statusCode = 200
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
            body["message"] = str(error)
            statusCode = 502
        # There was another error (likely our fault):
        except Exception as error:
            # Use default server error:
            body["message"] = str(error)
            statusCode = 500
        else:
            body["message"] = f"Sign in with {res.provider.capitalize()}"
            statusCode = 303
            headers["location"] = res.url
    else:
        body = { "message": "Unknown client error; please make sure the required parameters were provided." }
        statusCode = 400
          
    return body, statusCode, headers

# @bp.route('/logout')
def logout():
    sb = get_sb()
    
    # Default to an unknown server error:
    body = { "message": "An unknown error has occurred." }
    statusCode = 500
    
    try:
        res = sb.auth.sign_out()
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
    
    try:
        g.user.createProfile(requestBody)
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
    if res is not None:
        g.user = User(res.user)
    else:
        g.user = None
    