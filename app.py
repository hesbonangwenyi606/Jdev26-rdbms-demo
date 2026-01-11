# app.py
from flask import Flask, request, render_template_string, redirect, url_for
from rdbms.database import Database

app = Flask(__name__)
db = Database()

# Create demo table
db.create_table("users", ["id", "name"], [int, str], primary_key="id")

# HTML template with feedback messages and styling
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>RDBMS Web Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 50%; margin-bottom: 20px; }
        th, td { border: 1px solid #333; padding: 8px; text-align: left; }
        th { background-color: #555; color: white; }
        input[type=text], input[type=number] { padding: 5px; margin: 5px 0; }
        input[type=submit] { padding: 5px 10px; margin: 5px 0; }
        .message { color: green; font-weight: bold; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>Users Table</h1>
    {% if message %}
        <div class="message">{{ message }}</div>
    {% endif %}
    <table>
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
    message = request.args.get("message")
    return render_template_string(HTML, columns=table.columns, rows=rows, message=message)

@app.route("/add", methods=["POST"])
def add_user():
    table = db.get_table("users")
    id_val = int(request.form["id"])
    name = request.form["name"]
    try:
        table.insert([id_val, name])
        msg = f"User {name} added successfully."
    except ValueError:
        msg = f"Error: User with ID {id_val} already exists."
    return redirect(url_for("index", message=msg))

@app.route("/update", methods=["POST"])
def update_user():
    table = db.get_table("users")
    id_val = int(request.form["id"])
    name = request.form["name"]
    count = table.update(("id", id_val), {"name": name})
    msg = f"{count} row(s) updated." if count else f"No user found with ID {id_val}."
    return redirect(url_for("index", message=msg))

@app.route("/delete", methods=["POST"])
def delete_user():
    table = db.get_table("users")
    id_val = int(request.form["id"])
    count = table.delete(("id", id_val))
    msg = f"{count} row(s) deleted." if count else f"No user found with ID {id_val}."
    return redirect(url_for("index", message=msg))

if __name__ == "__main__":
    app.run(debug=True)
