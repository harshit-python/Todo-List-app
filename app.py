from flask import Flask, render_template, current_app, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Creating model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# Command to initialize database
@app.cli.command()
def init_db():
    with current_app.app_context():
        db.create_all()
        print("Database initialized.")
# init_db()


@app.route('/', methods=["GET"])
def home():
    queryset = Todo.query.all()
    return render_template("index.html", todo_list=queryset)


@app.route('/todo', methods=["GET", "POST"])
def list_create_todo():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['desc']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        queryset = Todo.query.all()
        return render_template("index.html", todo_list=queryset)
    if request.method == "GET":
        queryset = Todo.query.all()
        print(queryset)
        return render_template("index.html", todo_list=queryset)


@app.route('/delete/<int:sno>')
def retrieve_update_destroy(sno):
    todo_instance = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo_instance)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
