from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100), nullable=False)
    pengarang = db.Column(db.String(100), nullable=False)
    tahun = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Book {self.judul}>'
