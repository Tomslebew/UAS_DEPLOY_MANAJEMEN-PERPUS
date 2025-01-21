from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')  # Default key for local testing
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///library.db')  # Default to SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Database model
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100), nullable=False)
    pengarang = db.Column(db.String(100), nullable=False)
    tahun = db.Column(db.Integer, nullable=False)

# Forms
class BookForm(FlaskForm):
    judul = StringField('Judul Buku', validators=[DataRequired(), Length(max=100)])
    pengarang = StringField('Pengarang', validators=[DataRequired(), Length(max=100)])
    tahun = IntegerField('Tahun Terbit', validators=[DataRequired()])
    submit = SubmitField('Simpan')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Routes
@app.route('/')
def index():
    books = Books.query.all()
    return render_template('index.html', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == os.getenv('ADMIN_USERNAME', 'admin') and form.password.data == os.getenv('ADMIN_PASSWORD', 'password'):
            session['admin_logged_in'] = True
            flash('Berhasil login sebagai admin!', 'success')
            return redirect(url_for('index'))
        flash('Login gagal. Username atau password salah.', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Anda telah logout.', 'success')
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if not session.get('admin_logged_in'):
        flash('Login diperlukan.', 'error')
        return redirect(url_for('login'))
    form = BookForm()
    if form.validate_on_submit():
        new_book = Books(judul=form.judul.data, pengarang=form.pengarang.data, tahun=form.tahun.data)
        db.session.add(new_book)
        db.session.commit()
        flash('Buku berhasil ditambahkan!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    if not session.get('admin_logged_in'):
        flash('Login diperlukan.', 'error')
        return redirect(url_for('login'))
    book = Books.query.get_or_404(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.judul = form.judul.data
        book.pengarang = form.pengarang.data
        book.tahun = form.tahun.data
        db.session.commit()
        flash('Buku berhasil diperbarui!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    if not session.get('admin_logged_in'):
        flash('Login diperlukan.', 'error')
        return redirect(url_for('login'))
    book = Books.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Buku berhasil dihapus!', 'success')
    return redirect(url_for('index'))

# Database initialization route (only for local testing)
@app.route('/initdb')
def init_db():
    db.create_all()
    flash('Database initialized!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
