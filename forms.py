import datetime

from flask_wtf import Form
from wtforms import DateTimeField, IntegerField, PasswordField, TextField, TextAreaField 
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, 
                                Length, EqualTo)

from models import Entry


class create_entry(Form):
  title = TextField('Title',validators=[DataRequired()])
  date = DateTimeField('Date', default=datetime.datetime.now()) 
  time_spent = IntegerField('Time Spent in hours as an integer', validators=[DataRequired()])
  what_you_learned = TextAreaField('Something You Learned', validators=[DataRequired()])
  resources_to_remember = TextAreaField('Resources', validators=[DataRequired()])


class edit_entry(Form):
  title = TextField('Title',validators=[])
  date = DateTimeField('Date', default=Entry.date) 
  time_spent = TextField('Time Spent in hours as an integer', default=Entry.time_spent)
  what_you_learned = TextField('Something You Learned', default=Entry.what_you_learned)
  resources_to_remember = TextField('Resources', default=Entry.resources_to_remember)
