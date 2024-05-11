from flask import Flask
from flask import Flask, render_template, redirect, url_for, request, jsonify
from models.book import db, Book
from models.user import User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__, template_folder=os.path.abspath('Haidari/PycharmProjects/pythonProject2/templates'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Use your actual database URI
app.config['SECRET_KEY'] = 'asdfhj0843hyfoqifjrfu9054core'
db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


app = Flask(__name__)
@app.route('/')
def index():
    return 'Welcome to Library Management System'
if __name__ == '__main__':
    app.run(debug=True)


    def login():
        return render_template('login.html')


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/books/store', methods=['POST'])
    @login_required
    def add_book():
        if request.method == 'POST':
            data = request.form
            new_book = Book(
                title=data['title'],
                author=data['author'],
                publication_year=data['publication_year'],
                language=data['language']
            )
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('get_books'))
    def add_book():
        return redirect(url_for('get_books'))


    @app.route('/books/edit/<int:id>', methods=['GET'])
    @login_required
    def edit_book(id):
        book = Book.query.get(id)
        if book is None:
            return jsonify({'message': 'Book not found'}), 404
        return render_template('books/edit.html', book=book)