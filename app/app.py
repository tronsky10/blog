from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from model.user import db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SECRET_KEY'] = 'clave_secreta'
print("configuración de base de datos")
db.init_app(app)


class UserForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    email = StringField('Correo electrónico', validators=[
                        DataRequired(), Email()])
    submit = SubmitField('Añadir Usuario')


class RemoveUserForm(FlaskForm):
    username = StringField('Usuario a eliminar', validators=[DataRequired()])
    submit = SubmitField('Eliminar Usuario')


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/user_add', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))


# @app.route('/user_edit', methods=['POST'])
# def edit_user():
#    username = request.form['user.username']
#    user = User.query.filter_by(username=username).first()
#    if user:
#        user.verified = true
#        db.session.commit()  # Confirmar los cambios en la BD
#        print('el usuario ha sido modificado')
#        return redirect(url_for('index'))


@app.route('/user_remove', methods=['POST'])
def remove_user():
    username = request.form['user.username']
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)  # Elimina al usuario de la sesión
        db.session.commit()  # Confirmar los cambios en la BD
        print('el usuario ha sido borrado')
        return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.session.commit()
        db.create_all()

    app.run(debug=True, port=59)
