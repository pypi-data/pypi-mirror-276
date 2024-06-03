from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, Response
)
from werkzeug.security import generate_password_hash

# Bootstrap Budget Imports
from .auth import login_required, user_only
from .entities import User


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route("/")
@login_required
@user_only
def index() -> Response | str:
    return render_template('dashboard.html', user=g.user)


@bp.route("/update", methods=["POST"])
@login_required
def update() -> Response | str:
    """
    Update the current user from 'Edit Profile' modal.

    :return: Back to current view after update.
    """
    try:
        current_app.logger.info(request.form)
        g.user.first_name = request.form['first_name']
        g.user.middle_name = request.form['middle_name']
        g.user.last_name = request.form['last_name']
        g.user.address_line_1 = request.form['address_line_1']
        g.user.address_line_2 = request.form['address_line_2']
        g.user.city = request.form['city']
        g.user.state = request.form['state']
        g.user.zipcode = request.form['zipcode']
        g.user.email = request.form['email']
        g.user.phone_number = request.form['phone_number']

        flash('User profile was successfully saved.', 'info')
    except Exception as e:
        flash(f'User profile failed to save: {e}', 'error')

    return redirect(request.referrer)


@bp.route("/reset-password", methods=["POST"])
@login_required
def reset_password() -> Response | str:
    """
    Reset the password for a given user (by username) from 'Reset Password' modal.

    :return: Back to current view after update.
    """
    try:
        current_app.logger.info(request.form)
        username: str = request.form['username']
        user: User

        if g.user.username != username:
            user = User.get(username=request.form['username'])
        else:
            user = g.user

        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            user.hash = generate_password_hash(new_password)
            flash('User password was successfully changed.', 'info')
        else:
            flash('User password failed to change. Passwords did not match.', 'error')
    except Exception as e:
        flash(f'User password failed to be reset: {e}', 'error')

    return redirect(request.referrer)