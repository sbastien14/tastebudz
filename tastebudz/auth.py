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
#         "user_metadate": {},
#     }
# }
@bp.route('/user', methods=['POST'])
def register():
    username = request.form['username'] if request.form['username'] is not None else request.body['username']
    password = request.form['password'] if request.form['password'] is not None else request.body['password']
    sb = get_sb()
    
    # Default to an unknown server error:
    body = {
        "reason": "INTERNAL_SERVER_ERROR",
        "message": "An unknown error has occurred."
    }
    code = 500

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
            res = sb.auth.sign_up({
                "email": username,
                "password": password
            })
        except Exception as error:
            body["message"] = str(error)
        else:
            g.user = User(res.user)
            code = 201 # Successfully registered user
            # Check for email verification:
            if res.session is None:
                body = {
                    "reason": "EMAIL_ADDRESS_NOT_CONFIRMED",
                    "message": f"A verification email was sent to {username}. Please click the link in that email to verify you account.",
                    "user": g.user
                }
            else:
                body = {
                    "reason": "ACCOUNT_CREATION_SUCCESSFUL",
                    "message": f"{username} was successfully registered.",
                    "user": g.user
                }
            
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
    username = request.form['username']
    password = request.form['password']
    sb = get_sb()
    
    # Default to an unknown server error:
    body = {
        "reason": "INTERNAL_SERVER_ERROR",
        "message": "An unknown error has occurred."
    }
    code = 500
    
    if username is None:
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
            res = sb.auth.sign_in_with_password({"email": username, "password": password})
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