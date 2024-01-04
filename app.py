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
    tasks = db.relationship('Task', backref='user', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Ruta para agregar tarea
@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    new_task = Task(title=title, user=current_user)
    db.session.add(new_task)
    db.session.commit()

    # Guardar la tarea en el archivo en la carpeta instance
    with open(INSTANCE_FOLDER_PATH, 'a') as file:
        file.write(f"{title}\n")

    return redirect(url_for('index'))

# Ruta para la página de administración
@app.route('/admin')
@login_required
def admin():
    tasks = Task.query.filter_by(user=current_user).all()
    return render_template('admin.html', tasks=tasks)

# Ruta para agregar tarea desde la página de administración
@app.route('/admin/add', methods=['POST'])
@login_required
def add_task_admin():
    title = request.form['title']
    new_task = Task(title=title, user=current_user)
    db.session.add(new_task)
    db.session.commit()

    # Guardar la tarea en el archivo en la carpeta instance
    with open(INSTANCE_FOLDER_PATH, 'a') as file:
        file.write(f"{title}\n")

    return redirect(url_for('admin'))


@app.route('/admin/delete/<int:task_id>', methods=['GET'])
@login_required
def delete_task_admin(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete_all', methods=['GET'])
@login_required
def delete_all_tasks_admin():
    Task.query.delete()
    db.session.commit()
    return redirect(url_for('admin'))




   


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Crear la carpeta instance si no existe
    if not os.path.exists('instance'):
        os.makedirs('instance')

    # Iniciar la aplicación
    app.run(debug=True)