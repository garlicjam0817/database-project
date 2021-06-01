from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length

class PaitientRegistrationForm(FlaskForm):
    paitientID = IntegerField('ID',
                           validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    gender = StringField('Gender',
                        validators=[DataRequired(), Length(min=2, max=20) ])
    address = StringField('Address',
                        validators=[DataRequired(), Length(min=2, max=40)])
    date_of_birth = DateField('Date of Birth')
    zip_code = IntegerField('Zip Code', validators=[DataRequired()])
    county = StringField('County',
                        validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit')
