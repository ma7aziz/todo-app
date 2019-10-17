import os
from flask import Flask, render_template, flash,redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#app configuration

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')   #create database file


db = SQLAlchemy(app)


#database/table structure
class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(500))
    date = db.Column(db.Date)
    complete = db.Column(db.Boolean, default=False)


    def __init__(self, item, date):
        self.item = item
        self.date = date
        self.complete = False

    def __repr__(self):
        return f"{self.item}" ,f'{self.date}'


#create flask form
class todo_form(FlaskForm):
    item = StringField('To_Do')
    date = DateField('Date')
    submit  = SubmitField('Submit')


#main view
@app.route('/')
def index():

    form = todo_form()
    item = Todo.query.all()
    return render_template('index.html',form=form, item=item )




#submit
@app.route('/submit', methods = ['GET', 'POST'])
def submit():

    form = todo_form()
    item = Todo.query.all()
    if form.validate_on_submit():
        flash("ToDo item created")
        new_item = Todo (
           form.item.data,
           form.date.data
        )

        db.session.add(new_item)
        db.session.commit()
        item = Todo.query.all()
        return redirect('/')
    flash ("please fill all fields before submition :)")
    return redirect('/')




# remove
@app.route('/delete/<int:task_id>')
def remove(task_id):
    
    item = Todo.query.get(task_id)
    
    db.session.delete(item)
    db.session.commit()


    flash("Item deleted")
    return redirect('/')


# #complete 
@app.route('/complete/<int:task_id>')
def complete(task_id):
    item = Todo.query.get(task_id)
    if item.complete:
        item.complete = False
    else:
        item.complete = True
    
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug= True)
