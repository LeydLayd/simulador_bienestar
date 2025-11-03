from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User
from app import db
from decimal import Decimal

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    users = User.query.order_by(User.updated_at.desc()).all()
    return render_template('index.html', users=users)

@bp.route('/retirar/<int:id>', methods=['GET', 'POST'])
def retirar(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        try:
            amount = Decimal(request.form['amount'])
        except ValueError:
            flash('Por favor ingresa una cantidad válida.', 'error')
            return redirect(url_for('main.retirar', id=id))

        if amount <= 0:
            flash('La cantidad debe ser mayor que cero.', 'error')
        elif user.balance < amount:
            flash('Fondos insuficientes.', 'error')
        else:
            user.balance -= amount
            db.session.commit()
            flash(f'Retiro exitoso de ${amount:.2f}', 'success')
            return redirect(url_for('main.index'))

    return render_template('retirar.html', user=user)
