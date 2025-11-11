from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User
from app import db
from decimal import Decimal

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    users = User.query.first()
    return render_template('index.html', user=users)

@bp.route('/pin/<int:id>', methods=['GET', 'POST'])
def insertar_pin(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        pin_ingresado = request.form.get('pin')

        if not pin_ingresado:
            flash('Por favor, ingresa tu PIN.', 'error')
            return redirect(url_for('main.insertar_pin', id=id))

        if pin_ingresado == user.pin:
            flash('PIN correcto. Bienvenido.', 'success')
            return redirect(url_for('main.opciones',id=id))
        else:
            flash('PIN incorrecto. Inténtalo de nuevo.', 'error')
            return redirect(url_for('main.insertar_pin', id=id))

    return render_template('pin.html', user=user)


@bp.route('/opciones/<int:id>')
def opciones(id):
    user = User.query.get_or_404(id)
    return render_template('opciones.html', user=user)

@bp.route('/consulta/<int:id>')
def consulta(id):
    user = User.query.get_or_404(id)
    return render_template('consulta.html', user=user)

@bp.route('/cambio')
def cambio():
    return render_template('cambio.html')

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
            return redirect(url_for('main.opciones',id=id))

    return render_template('retirar.html', user=user)
