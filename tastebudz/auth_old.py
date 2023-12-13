from functools import wraps
from flask import (
    Blueprint, flash, g, redirect, make_response, request, url_for
)
from gotrue.errors import AuthApiError
from tastebudz.sb import get_sb
from tastebudz.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

# API Response format ("user" field only present in successful account creation):
# {
#     "reason": "BRIEF_DESCRIPTION",
#     "message": "Long description for displaying if needed.",
#     "user": {
#         "id": "2fh390dfd-34832894hd-834gdfhb",
#         "email": "email@example.com",
#         "phone": "555-123-4444",
#         "role": "authenticated",
#         "user_metadata": {},
#     }
# }
@bp.route('/user', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    role = request.form.get('role', 0)
    firstName = request.form.get('first_name')
    lastName = request.form.get('last_name')
    dob = request.form.get('dob')
    phone = request.form.get('phone')
    
    # Default to an unknown server error:
    body = {
        "reason": "INTERNAL_SERVER_ERROR",
        "message": "An unknown error has occurred."
    }
    code = 500
    sb = get_sb()
    
    if username or password:
        if not username:
            body = {
                "reason": "INVALID_ACCOUNT_INFORMATION",
                "message": "Username is required but was not provided."
            }
        elif not password:
            body = {
                "reason": "INVALID_ACCOUNT_INFORMATION",
                "message": "Password is required but was not provided."
            }
        else:
            try:
                # Create user account:
                res = sb.auth.sign_up({
                    "email": email,
                    "password": password
                })
                print(res.user.id)
                # Add user profile data:
                g.profile = {
                    "id": res.user.id,
                    "username": username,
                    "first_name": firstName,
                    "last_name": lastName,
                    "dob": dob
                }
                # data, count = sb.table('user_profiles').insert({
                #     "id": res.user.id,
                #     "username": username,
                #     "first_name": firstName,
                #     "last_name": lastName,
                #     "dob": dob
                # }).execute()
            except Exception as error:
                body["message"] = str(error)
            else:
                g.user = User(res.user)
                code = 201 # Successfully registered user
                # Check for email verification:
                if res.session is None:
                    body = {
                        "reason": "EMAIL_ADDRESS_NOT_CONFIRMED",
                        "message": f"A verification email was sent to {email}. Please click the link in that email to verify you account.",
                        "user": g.user
                    }
                else:
                    body = {
                        "reason": "ACCOUNT_CREATION_SUCCESSFUL",
                        "message": f"{username} was successfully registered.",
                        "user": g.user
                    }
    else:
        # Did not receive valid form data:
        body = {
            "reason": "BAD_REQUEST",
            "message": "Invalid form data submitted."
        }
        code = 400
                
    return make_response(body, code)
            

# API Response format ("user" field only present in successful login):
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
@bp.route('/user', methods=['GET'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    oauth_provider = request.form.get('oauth_provider')
    access_token = request.form.get('access_token')
    refresh_token = request.form.get('refresh_token')
    sb = get_sb()
    
    # Default to an unknown server error:
    body = {
        "reason": "INTERNAL_SERVER_ERROR",
        "message": "An unknown error has occurred."
    }
    code = 500
    
    # Authenticate with OAuth:
    if oauth_provider is not None:
        # OAuth process has returned from provider with access token:
        if access_token and refresh_token:
            try:
                res = sb.auth.set_session(access_token, refresh_token)
                if g.profile:
                    data, count = sb.table('user_profiles').insert(g.pop('profile')).execute()
            # Supabase API returned an error:
            except AuthApiError as error:
                body = {
                    "reason": "USER_AUTHENTICATION_ERROR",
                    "message": str(error)
                }
            # There was another error (likely our fault):
            except Exception as error:
                # Use default server error:
                body["message"] = str(error)
            # No errors, we're signed in!
            else:
                g.user = User(res.user)
                body = {
                    "reason": "USER_AUTHENTICATION_SUCCESSFUL",
                    "message": f"Successfully signed in {username}.",
                    "user": g.user
                }
                code = 200
        # Return redirect URL for OAuth with requested provider:
        else:
            try:
                res = sb.auth.sign_in_with_oauth({
                    "provider": oauth_provider
                })
            # Supabase API returned an error:
            except AuthApiError as error:
                body = {
                    "reason": "USER_AUTHENTICATION_ERROR",
                    "message": str(error)
                }
                code = 500
            # There was another error (likely our fault):
            except Exception as error:
                # Use default server error:
                body["message"] = str(error)
            else:
                print(res)
                # redirect(res.url)
                body = {
                    "reason": "REDIRECT_FOR_OAUTH",
                    "message": f"Sign in with {res.provider.capitalize()}",
                    "redirect": res.url
                    # "user": res
                }
                code = 303
    elif email is None:
        body = {
            "reason": "INVALID_USER_AUTHENTICATION",
            "message": "Email is required but was not provided."
        }
        code = 400
    elif password is None:
        body = {
            "reason": "INVALID_USER_AUTHENTICATION",
            "message": "Password is required but was not provided."
        }
        code = 400
    # We have username and password, now let's try logging in:
    else:
        try:
            res = sb.auth.sign_in_with_password({"email": email, "password": password})
            if g.profile:
                    data, count = sb.table('user_profiles').insert(g.pop('profile')).execute()
        # The Supabase API returned an error:
        except AuthApiError as error:
            body = {
                "reason": "USER_AUTHENTICATION_ERROR",
                "message": str(error)
            }
            code = 500
        # There was another error (likely our fault):
        except Exception as error:
            # Use default server error:
            body["message"] = str(error)
        # No errors, we are signed in:
        else:
            g.user = User(res.user)
            body = {
                "reason": "USER_AUTHENTICATION_SUCCESSFUL",
                "message": f"Successfully signed in {username}.",
                "user": g.user
            }
            code = 200
    
    # If successfully signed in (auth API returns a valid response), login:
    # if res is not None:
    #     g.user = User(res.user)
    #     body = {
    #         "reason": "USER_AUTHENTICATION_SUCCESSFUL",
    #         "message": f"Successfully signed in {username}.",
    #         "user": g.user
    #     }
    #     code = 200
            
    return make_response(body, code)


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
@bp.route('/logout')
def logout():
    sb = get_sb()
    
    # Default to an unknown server error:
    body = {
        "reason": "INTERNAL_SERVER_ERROR",
        "message": "An unknown error has occurred."
    }
    code = 500
    
    try:
        res = sb.auth.sign_out()
    except AuthApiError as error:
        body = {
            "reason": "USER_AUTHENTICATION_ERROR",
            "message": str(error)
        }
    except Exception as error:
        body["message"] = str(error)
    else:
        oldUser = g.pop('user')
        body = {
            "reason": "LOGOUT_SUCCESSFUL",
            "message": f"Successfully logged out {oldUser.email}.",
            "user": oldUser
        }
        code = 200
        
    return make_response(body, code)


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