from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    checked = db.Column(db.Boolean, default=False)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    try:
        if request.method == "POST":
            todo_name = request.form["todo_name"]
            new_todo = Todo(name=todo_name)
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for("home"))
        todos = Todo.query.all()
        return render_template("index.html", items=todos)
    except Exception as e:

        return render_template("index.html", error=str(e))

@app.route("/checked/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    try:
        todo = Todo.query.get_or_404(todo_id)
        todo.checked = not todo.checked
        db.session.commit()
        return redirect(url_for("home"))
    except NoResultFound:
        return render_template("index.html", error="Todo not found.")

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    try:
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("home"))
    except NoResultFound:
        return render_template("index.html", error="Todo not found.")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

