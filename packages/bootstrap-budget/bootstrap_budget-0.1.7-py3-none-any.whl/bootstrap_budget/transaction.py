from flask import (
    Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)

# Bootstrap Budget Imports
from .auth import login_required, user_only


bp = Blueprint('transaction', __name__, url_prefix='/transactions')


@bp.route("/")
@login_required
@user_only
def index() -> Response | str:
    return render_template('transaction.html', user=g.user)
