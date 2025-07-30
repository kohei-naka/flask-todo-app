from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

class TodoForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired()])
    due_date = DateField('期限', format='%Y-%m-%d', validators=[DataRequired()])
    priority = SelectField('優先度', choices=[
        (3, '高'),
        (2, '中'),
        (1, '低')
    ], coerce=int, validators=[DataRequired()])
    submit = SubmitField('追加')
