from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class BookForm(FlaskForm):
    judul = StringField('Judul Buku', validators=[DataRequired(), Length(max=100)])
    pengarang = StringField('Pengarang', validators=[DataRequired(), Length(max=100)])
    tahun = IntegerField('Tahun Terbit', validators=[DataRequired()])
    submit = SubmitField('Simpan')
