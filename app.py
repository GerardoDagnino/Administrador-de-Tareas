from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

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
    start_date = db.Column(db.Date)

# Ruta para obtener las tareas en formato JSON para FullCalendar
@app.route('/admin/tasks')
@login_required
def get_tasks():
    tasks = Task.query.all()
    events = [{"title": task.title, "start": task.start_date.isoformat()} for task in tasks]
    return {"tasks": events}

# Ruta para añadir una nueva tarea
@app.route('/admin/add', methods=['POST'])
@login_required
def add_task_admin():
    title = request.form['title']
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('admin'))

# Ruta para eliminar una tarea por su ID
@app.route('/admin/delete/<int:task_id>', methods=['GET'])
@login_required
def delete_task_admin(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('admin'))

# Ruta para eliminar todas las tareas
@app.route('/admin/delete_all', methods=['GET'])
@login_required
def delete_all_tasks_admin():
    Task.query.delete()
    db.session.commit()
    return redirect(url_for('admin'))

# Ruta para el administrador de tareas
@app.route('/admin')
@login_required
def admin():
    tasks = Task.query.all()
    return render_template('admin.html', tasks=tasks)

# Ruta para cerrar sesión en el administrador de tareas
@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    