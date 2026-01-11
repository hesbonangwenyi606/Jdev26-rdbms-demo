# app.py
from flask import Flask, request, render_template_string, redirect
from rdbms.database import Database

app = Flask(__name__)
db = Database()

# Create a table for demo
db.create_table("users", ["id", "name"], [int, str], primary_key="id")

# HTML template
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>RDBMS Web Demo</title>
</head>
<body>
    <h1>Users Table</h1>
    <table border="1">
        <tr>
        {% for col in columns %}
            <th>{{ col }}</th>
        {% endfor %}
        </tr>
        {% for row in rows %}
        <tr>
            {% for col in columns %}
            <td>{{ row[col] }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>

    <h2>Add User</h2>
    <form method="post" action="/add">
        ID: <input type="number" name="id" required>
        Name: <input type="text" name="name" required>
        <input type="submit" value="Add">
    </form>

    <h2>Update User Name</h2>
    <form method="post" action="/update">
        ID: <input type="number" name="id" required>
        New Name: <input type="text" name="name" required>
        <input type="submit" value="Update">
    </form>

    <h2>Delete User</h2>
    <form method="post" action="/delete">
        ID: <input type="number" name="id" required>
        <input type="submit" value="Delete">
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    table = db.get_table("users")
    rows = table.select()
    return render_template_string(HTML, columns=table.columns, rows=rows)

@app.route("/add", methods=["POST"])
def add_user():
    table = db.get_table("users")
    id_val = int(request.form["id"])
    name = request.form["name"]
    try:
        table.insert([id_val, name])
    except ValueError as e:
        pass  # ignore duplicates
    return redirect("/")

@app.route("/update", methods=["POST"])
def update_user():
    table = db.get_table("users")
    id_val = int(request.form["id"])
    name = request.form["name"]
    table.update(("id", id_val), {"name": name})
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete_user():
    table = db.get_table("users")
    id_val = int(request.form["id"])
    table.delete(("id", id_val))
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
