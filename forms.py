from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired

class MenuItemForm(FlaskForm):
    name = StringField('Назва', validators=[DataRequired()])
    description = TextAreaField('Опис', validators=[DataRequired()])
    price = FloatField('Ціна', validators=[DataRequired()])
    submit = SubmitField('Зберегти')