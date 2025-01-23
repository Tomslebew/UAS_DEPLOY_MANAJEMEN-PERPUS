from flask_sqlalchemy import SQLAlchemy

# Inisialisasi SQLAlchemy
db = SQLAlchemy()

# Definisi Model Buku
class Book(db.Model):
    __tablename__ = 'books'  # Nama tabel dalam database
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100), nullable=False, index=True)
    pengarang = db.Column(db.String(100), nullable=False, index=True)
    tahun = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Book {self.judul}>'
