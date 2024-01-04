import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Definir la ruta al archivo en la carpeta instance
INSTANCE_FOLDER_PATH = os.path.join('instance', 'tasks.txt')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)

# Resto del código...

# Ruta para agregar tarea desde la página de administración
@app.route('/admin/add', methods=['POST'])
@login_required
def add_task_admin():
    title = request.form['title']
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()

    # Guardar la tarea en el archivo en la carpeta instance
    with open(INSTANCE_FOLDER_PATH, 'a') as file:
        file.write(f"{title}\n")

    return redirect(url_for('admin'))