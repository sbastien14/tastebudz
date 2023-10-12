from functools import wraps
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from tastebudz.sb import get_sb

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sb = get_sb()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                res = sb.auth.sign_up({
                    "email": username,
                    "password": password
                })
                # Check for email verification:
                if res.session is None:
                    flash(f"A verification email was sent to {username}. Please click the link in that email to verify you account.")
                return redirect(url_for("auth.login"))
            except Exception as e:
                error = e

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sb = get_sb()
        error = None

        try:
            res = sb.auth.sign_in_with_password({"email": username, "password": password})
        except:
            error = "Invalid username or password."

        if error is None:
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    sb = get_sb()
    try:
        res = sb.auth.get_user()
        g.user = res.user
    except:
        g.user = None
        
@bp.route('/logout')
def logout():
    sb = get_sb()
    res = sb.auth.sign_out()
    flash("You have successfully logged out!")
    return redirect(url_for('auth.login'))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("You must be logged in to see this page.")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view