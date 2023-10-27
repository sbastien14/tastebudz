from functools import wraps
from flask import (
    Blueprint, flash, g, redirect, make_response, request, url_for
)
from gotrue.errors import AuthApiError
from tastebudz.sb import get_sb
from tastebudz.models import User
import json

bp = Blueprint('auth', __name__, url_prefix='/auth')

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
            print(res.user)
        except AuthApiError as error:
            body["message"] = str(error)
            statusCode = 502
        except Exception as error:
            body["message"] = str(error)
            statusCode = 500
        else:
            g.user = User(res.user)
            # Awaiting email verification:
            if res.session is None:
                body['message'] = 'Account created; awaiting email verification.'
                body['user'] = g.user
                statusCode = 202
            # User account created successfully:
            else:
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
def login(oauth_provider:str=None, access_token:str=None, refresh_token:str=None):
    email = request.authorization.username
    password = request.authorization.password
    sb = get_sb()
    
    # Default to an unknown server error:
    body = { "message": "An unknown error has occurred." }
    statusCode = 500
    headers = {}
    
    # Authenticate with OAuth:
    if oauth_provider is not None:
        # OAuth process has returned from provider with access token:
        if access_token and refresh_token:
            try:
                res = sb.auth.set_session(access_token, refresh_token)
                # if g.profile:
                #     data, count = sb.table('user_profiles').insert(g.pop('profile')).execute()
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
                    "message": f"Successfully signed in {g.user.username}.",
                    "user": g.user
                }
                statusCode = 200
        # Return redirect URL for OAuth with requested provider:
        else:
            try:
                res = sb.auth.sign_in_with_oauth({
                    "provider": oauth_provider
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
    elif email is None:
        body["message"] = "Email is required but was not provided."
        statusCode = 400
    elif password is None:
        body["message"] = "Password is required but was not provided."
        statusCode = 400
    # We have username and password, now let's try logging in:
    else:
        try:
            res = sb.auth.sign_in_with_password({"email": email, "password": password})
            # if g.profile:
            #         data, count = sb.table('user_profiles').insert(g.pop('profile')).execute()
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
            
    return body, statusCode, headers


# API Response format ("user" field only present in successful logout):
# {
#     "reason": "BRIEF_DESCRIPTION",
#     "message": "Long description for displaying if needed.",
#     "user": {
#         "id": "2fh390dfd-34832894hd-834gdfhb",
#         "email": "email@example.com",
#         "phone": "555-123-4444",
#         "role": "authenticated",
#         "user_metadate": {},
#     }
# }
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
        try:
            oldUser:User = g.pop('user')
            body = {
                "message": f"Successfully logged out {oldUser.username or oldUser.email}.",
                "user": oldUser
            }
            statusCode = 200
        except:
            body = {
                "message": "Successfully logged out.",
                "user": {}
            }
            statusCode = 200
        
    return body, statusCode


@bp.before_app_request
def load_logged_in_user():
    sb = get_sb()
    try:
        res = sb.auth.get_user()
        g.user = User(res.user)
    except:
        g.user = None


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("You must be logged in to see this page.")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view