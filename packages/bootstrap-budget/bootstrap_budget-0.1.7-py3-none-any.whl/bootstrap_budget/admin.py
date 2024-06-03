import os
import signal

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, Response, session, url_for
)
from werkzeug.security import check_password_hash

# Import bootstrap-budget blueprints/modules/classes/functions
from .auth import login_required, admin_only


bp = Blueprint('admin', __name__, url_prefix='/admin')


# TODO: Enable user registration
# - Adds a link for self registration on the login page
# - Otherwise users can only be added through the admin console
# - Default is unchecked
# - Not editable at the moment
# - Add as config?


@bp.route("/")
@login_required
@admin_only
def index() -> Response | str:
    return render_template('admin.html', user=g.user)


@bp.route("/users")
@login_required
@admin_only
def users() -> Response | str:
    return render_template('user_admin.html', user=g.user)


@bp.route("/shutdown", methods=['POST'])
@login_required
@admin_only
def shutdown() -> None:
    if request.method == 'POST':
        current_app.logger.info('Admin password checks out. Trying to shutdown...')
        #os.kill(os.getpid(), signal.SIGINT)
