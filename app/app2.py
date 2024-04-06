from flask import Flask, render_template, request, redirect, url_for
from model.user import db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
print("configuración de base de datos")

db.init_app(app)


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
