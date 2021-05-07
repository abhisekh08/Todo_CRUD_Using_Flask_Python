from flask import Flask, render_template, redirect, request
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Model Creation
class Todos(db.Model):
    slno = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(50), nullable = False)
    desc = db.Column(db.String(200), nullable = False )
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return "{} - {}".format(self.slno, self.title)

# check if the db is already created or not        
dirlst = os.listdir()
print(dirlst)
if ("todos.db" not in dirlst):
    # create the 
    db.create_all()
    print("Database todos.db created successfully")

# Home route
@app.route('/',methods=["GET","POST"])
def index():
    if request.method == 'POST':
        title = request.form["title"]
        description = request.form["desc"]
        todo = Todos(title = title, desc = description)
        db.session.add(todo)
        db.session.commit()

    todolist = Todos.query.all()
    return render_template("index.html",page = "Home", todolist = todolist) 

# View the todo list
@app.route("/view")
def viewer():
    todolist = Todos.query.all()
    return render_template("index.html",page = "Home", todolist = todolist) 


# Update route
@app.route('/update/<int:slno>', methods=['GET','POST'])
def update(slno):
    if request.method == 'POST':
        title = request.form["title"]
        description = request.form["desc"]
        todo = Todos.query.filter_by(slno = slno).first()
        todo.title = title
        todo.desc = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todos.query.filter_by(slno = slno).first()
    return render_template("update.html", page = "update", todo = todo)

# Delete Route
@app.route('/delete/<int:slno>', methods=['GET','POST'])
def delete(slno):
    todo = Todos.query.filter_by(slno = slno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# About page route
@app.route('/about')
def about():
    return render_template("about.html", page="about")

if __name__ == "__main__":
    app.run(debug=True,port=8000)