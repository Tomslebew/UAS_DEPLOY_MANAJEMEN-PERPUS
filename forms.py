from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class BookForm(FlaskForm):
    # Field untuk judul buku
    judul = StringField(
        'Judul Buku',
        validators=[
            DataRequired(message="Judul buku wajib diisi."),
            Length(max=100, message="Judul buku tidak boleh lebih dari 100 karakter.")
        ]
    )
    
    # Field untuk pengarang buku
    pengarang = StringField(
        'Pengarang',
        validators=[
            DataRequired(message="Nama pengarang wajib diisi."),
            Length(max=50, message="Nama pengarang tidak boleh lebih dari 50 karakter.")
        ]
    )
    
    # Field untuk tahun terbit
    tahun = IntegerField(
        'Tahun Terbit',
        validators=[
            DataRequired(message="Tahun terbit wajib diisi."),
            NumberRange(min=1900, max=2100, message="Tahun terbit harus antara 1900 dan 2100.")
        ]
    )
    
    # Tombol submit
    submit = SubmitField('Simpan')
