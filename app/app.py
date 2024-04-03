from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/add', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.session.commit()
        db.create_all()

    app.run(debug=True, port=59)