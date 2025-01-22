import os
import requests
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

# URL File SQL
SQL_FILE_URL = "https://raw.githubusercontent.com/Saimonaligok/data/refs/heads/main/library_db.sql"
SQL_FILE_NAME = "library_db.sql"

# Fungsi untuk mengunduh dan mengimpor file SQL
def setup_database():
    try:
        # Unduh file SQL
        response = requests.get(SQL_FILE_URL)
        response.raise_for_status()
        with open(SQL_FILE_NAME, "wb") as file:
            file.write(response.content)

        # Impor file SQL ke database MySQL
        subprocess.run(f"mysql -u root -p library_db < {SQL_FILE_NAME}", shell=True, check=True)
        print("Database berhasil diperbarui.")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengunduh atau mengimpor database: {e}")

# Jalankan setup database
setup_database()

# Konfigurasi Flask
app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/library_db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Model Database
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100), nullable=False)
    pengarang = db.Column(db.String(100), nullable=False)
    tahun = db.Column(db.Integer, nullable=False)

    def _repr_(self):
        return f'<Book {self.judul}>'

# Form Tambah Buku
class BookForm(FlaskForm):
    judul = StringField('Judul Buku', validators=[DataRequired(), Length(max=100)])
    pengarang = StringField('Pengarang', validators=[DataRequired(), Length(max=100)])
    tahun = IntegerField('Tahun Terbit', validators=[DataRequired()])
    submit = SubmitField('Simpan')

# Form Login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Rute Utama
@app.route('/')
def index():
    books = Books.query.all()
    return render_template('index.html', books=books)

# Rute Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'saimona' and form.password.data == 'saimona123':
            session['admin_logged_in'] = True
            flash('Berhasil login sebagai admin!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login gagal. Periksa username dan password.', 'error')
    return render_template('login.html', form=form)

# Rute Logout
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Anda telah logout.', 'success')
    return redirect(url_for('index'))

# Rute Tambah Buku
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if not session.get('admin_logged_in'):
        flash('Anda harus login terlebih dahulu.', 'error')
        return redirect(url_for('login'))

    form = BookForm()
    if form.validate_on_submit():
        new_book = Books(
            judul=form.judul.data,
            pengarang=form.pengarang.data,
            tahun=form.tahun.data
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Buku berhasil ditambahkan!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

# Rute Edit Buku
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    if not session.get('admin_logged_in'):
        flash('Anda harus login terlebih dahulu.', 'error')
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

# Rute Hapus Buku
@app.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    if not session.get('admin_logged_in'):
        flash('Anda harus login terlebih dahulu.', 'error')
        return redirect(url_for('login'))

    book = Books.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Buku berhasil dihapus!', 'success')
    return redirect(url_for('index'))

# Jalankan Aplikasi
if _name_ == '_main_':
    app.run(debug=True)
