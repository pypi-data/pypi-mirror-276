from datetime import datetime
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, Response
)

# Bootstrap Budget Imports
from .auth import login_required, user_only
from .entities import Account


bp = Blueprint('account', __name__, url_prefix='/accounts')


@bp.route("/")
@login_required
@user_only
def index() -> Response | str:
    # Query account records
    accounts = Account.select(user_id=g.user, is_active=True).order_by(Account.name)

    return render_template('account.html', user=g.user, accounts=accounts)


@bp.route("/create", methods=["POST"])
@login_required
def create() -> Response | str:
    """
    Create a new Account from the 'Create Account' modal.

    :return: Back to current view after creation.
    """
    try:
        current_app.logger.info(request.form)

        Account(name=request.form['name'],
                description=request.form['description'],
                account_number=request.form['account_number'],
                account_route_nbr=request.form['account_route_nbr'],
                opening_amount=float(request.form['opening_amount']),
                created_dt_tm=datetime.now(),
                updated_dt_tm=datetime.now(),
                user_id=g.user.id)

        flash('The account was successfully created.', 'info')
    except Exception as e:
        flash(f'The account failed to be created: {e}', 'error')

    return redirect(request.referrer)


@bp.route("/update", methods=["POST"])
@login_required
def update() -> Response | str:
    """
    Update the current account from the 'Update Account' modal.

    :return: Back to current view after update.
    """
    try:
        current_app.logger.info(request.form)

        account_id: int = int(request.form['id'])
        Account[account_id].set(name=request.form['name'],
                                description=request.form['description'],
                                account_number=request.form['account_number'],
                                account_route_nbr=request.form['account_route_nbr'],
                                opening_amount=float(request.form['opening_amount']),
                                updated_dt_tm=datetime.now())

        flash('The account was successfully updated.', 'info')
    except Exception as e:
        flash(f'The account failed to update: {e}', 'error')

    return redirect(request.referrer)


@bp.route("/delete", methods=["POST"])
@login_required
def delete() -> Response | str:
    """
    Delete an account.

    :return: Back to current view after deletion.
    """
    try:
        current_app.logger.info(request.form)

        account_id: int = int(request.form['id'])
        Account[account_id].delete()

        flash('The account was successfully deleted.', 'info')
    except Exception as e:
        flash(f'The account failed to delete: {e}', 'error')

    return redirect(request.referrer)
