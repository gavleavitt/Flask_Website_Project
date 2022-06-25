from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length

class processActForm(FlaskForm):
    activityID = StringField('ActivityID', [DataRequired(),
                                            Length(max=10,
                                            message=("Check that the provided ID is correct"))])
submit = SubmitField('Submit')