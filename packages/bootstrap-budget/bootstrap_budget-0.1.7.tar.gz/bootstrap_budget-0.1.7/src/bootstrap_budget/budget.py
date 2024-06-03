from datetime import datetime
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, Response
)
from pony import orm

# Bootstrap Budget Imports
from .auth import login_required, user_only
from .entities import Budget


bp = Blueprint('budget', __name__, url_prefix='/budgets')


@bp.route("/")
@login_required
@user_only
def index() -> Response | str:
    # Query budget records
    budgets = Budget.select(user_id=g.user, is_active=True).order_by(orm.desc(Budget.budget_year), Budget.name)

    return render_template('budget.html', user=g.user, budgets=budgets)


@bp.route("/create", methods=["POST"])
@login_required
def create() -> Response | str:
    """
    Create a new Budget from the 'Create Budget' modal.

    :return: Back to current view after update.
    """
    try:
        Budget(name=request.form['name'],
               description=request.form['description'],
               budget_year=int(request.form['budget_year']),
               created_dt_tm=datetime.now(),
               updated_dt_tm=datetime.now(),
               user_id=g.user.id)

        flash('The budget was successfully created.', 'info')
    except Exception as e:
        flash(f'The budget failed to be created: {e}', 'error')

    return redirect(request.referrer)


@bp.route("/update", methods=["POST"])
@login_required
def update() -> Response | str:
    """
    Update the current budget from the 'Update Budget' modal.

    :return: Back to current view after update.
    """
    try:
        current_app.logger.info(request.form)

        budget_id: int = int(request.form['id'])
        Budget[budget_id].set(name=request.form['name'],
                              description=request.form['description'],
                              budget_year=int(request.form['budget_year']),
                              updated_dt_tm=datetime.now())

        flash('The budget was successfully saved.', 'info')
    except Exception as e:
        flash(f'The budget failed to save: {e}', 'error')

    return redirect(request.referrer)


@bp.route("/delete", methods=["POST"])
@login_required
def delete() -> Response | str:
    """
    Delete a budget.

    :return: Back to current view after deletion.
    """
    try:
        current_app.logger.info(request.form)

        budget_id: int = int(request.form['id'])
        Budget[budget_id].delete()

        flash('The budget was successfully saved.', 'info')
    except Exception as e:
        flash(f'The budget failed to save: {e}', 'error')

    return redirect(request.referrer)
