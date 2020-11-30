from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask import render_template

import datetime
import forms
import models

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'a'


@app.before_request
def before_request():
  """Connect to the database before each request."""
  g.db = models.DATABASE
  g.db.connect()
  
  
@app.after_request
def after_request(response):
  """Close the database connection after each request."""
  g.db.close()
  return response


@app.route('/')
@app.route('/entries', methods=('GET', 'POST'))
def index():
  entries = models.Entry.select()
  return render_template('index.html', entries=entries)


def first_entry():
  try:
      entry = models.Entry.get(models.Entry.title == "Greetings")
  except models.DoesNotExist:
    models.Entry.create(
        title='Greetings',
        time_spent='1',
        what_you_learned='A great deal.',
        resources_to_remember='treehouse, python.org, stackoverflow.com, and djangoproject.com.'
    )


@app.route('/entries/new', methods=('GET', 'POST'))  
def create():
  """This line accesses the form for the html to read the fields."""
  form = forms.create_entry()
  if form.validate_on_submit():
      flash("Your entry has been posted.", "info")
      models.Entry.create(
        title=form.title.data,
        date=form.date.data,
        time_spent=form.time_spent.data,
        what_you_learned=form.what_you_learned.data,
        resources_to_remember=form.resources_to_remember.data
      )
      return redirect(url_for('index'))
    
  flash("Your entry was not posted.", "error")  
  return render_template('new.html', form=form)


@app.route('/entries/<int:id>', methods=['GET']) 
def detail(id):
  try:
    entry = models.Entry.get(models.Entry.id == id)
  except models.DoesNotExist:
    return render_template('404.html')
    
  return render_template('detail.html', entry=entry)


@app.route('/entries/<int:id>/edit', methods=('GET', 'POST')) 
def update(id):
  try:
      entry = models.Entry.get(models.Entry.id == id)
  except models.DoesNotExist:
      return render_template('404.html')

  form = forms.edit_entry()

  if form.validate_on_submit():
      entry.title = form.title.data
      entry.date = form.date.data
      entry.time_spent = form.time_spent.data
      entry.what_you_learned = form.what_you_learned.data
      entry.resources_to_remember = form.resources_to_remember.data
      entry.save()
      return redirect(url_for('index'))
  return render_template('edit.html', entry=entry, form=form)


@app.route('/entries/<int:id>/delete') 
def delete(id):
  try:
      models.Entry.get(models.Entry.id == id).delete_instance()
  except models.DoesNotExist:
      return render_template('404.html')
  return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    first_entry()
    app.run(debug=DEBUG, port=PORT, host=HOST)
