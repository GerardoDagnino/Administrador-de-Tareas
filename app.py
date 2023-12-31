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
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)

@app.route('/admin/tasks')
@login_required
def get_tasks():
    tasks = Task.query.all()
    events = []
    for task in tasks:
        events.append({
            'title': task.title,
            'start': task.start_date.isoformat(),
            'end': task.end_date.isoformat() if task.end_date else None
        })
    return jsonify({'tasks': events})

# Resto del código (mantén las rutas existentes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)