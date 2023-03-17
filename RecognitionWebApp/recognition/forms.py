from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField


class RecognitionForm(FlaskForm):
    picture = FileField('Picture to be recognized', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Recognize')