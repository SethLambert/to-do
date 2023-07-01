from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import exc
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
db = SQLAlchemy()
db.init_app(app)

#API Key
API_KEY = "funWITHapiCODE"

##Cafe TABLE Configuration
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(250), unique=True, nullable=False)
    complete = db.Column(db.Boolean, nullable=False, default = False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()
    
class ToDoForm(FlaskForm):
    todo = StringField('What do you need to do?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/", methods=["GET", "POST"])
def home():
    form = ToDoForm()
    if request.method == 'POST':
        new_to_do = Todo(
            todo = request.form.get('todo')
        )
        try:
            db.session.add(new_to_do)
            db.session.commit()
            return redirect(url_for('home'))
        except exc.IntegrityError:
            pass    
    to_do_list = db.session.query(Todo).all()
    list_of_rows = []
    for row in to_do_list:
        list_of_rows.append(row)
    return render_template("index.html", form=form, to_do_list=list_of_rows)

@app.route("/delete/<int:id>", methods=["GET","POST"])
def delete(id):
    with app.app_context():
        to_do_item = Todo.query.get(id)
    if to_do_item:
        with app.app_context():
            db.session.delete(to_do_item)
            db.session.commit()
    return redirect(url_for('home'))

@app.route("/complete/<int:id>", methods=["GET","POST"])
def complete(id):
    try:
        with app.app_context():
            to_do_item = Todo.query.get(id)
            if to_do_item.complete == True:
                to_do_item.complete = False
            else:
                to_do_item.complete = True
            db.session.commit()
    except AttributeError:
        pass
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
