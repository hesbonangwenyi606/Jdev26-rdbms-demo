# app.py
from flask import Flask, request, jsonify, render_template_string
from rdbms.database import Database

app = Flask(__name__)
db = Database()

# Create demo table
db.create_table("users", ["id", "name"], primary_key="id")

# HTML template with dynamic JS and centered layout
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>RDBMS Web Demo</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: flex-start; 
            min-height: 100vh; 
            background-color: #f4f4f4;
        }
        h1, h2 { text-align: center; }
        table { 
            border-collapse: collapse; 
            width: 50%; 
            margin-bottom: 20px; 
            background-color: white;
        }
        th, td { border: 1px solid #333; padding: 8px; text-align: left; }
        th { background-color: #555; color: white; }
        form { 
            background-color: white; 
            padding: 10px 15px; 
            margin-bottom: 15px; 
            border-radius: 5px; 
            box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
        }
        input[type=text], input[type=number] { padding: 5px; margin: 5px 0; }
        input[type=submit] { padding: 5px 10px; margin: 5px 0; }
        .message { 
            color: green; 
            font-weight: bold; 
            margin-bottom: 20px; 
            text-align: center; 
        }
    </style>
</head>
<body>
    <h1>Users Table</h1>
    <div id="message" class="message"></div>
    <table id="users-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

    <h2>Add User</h2>
    <form id="add-form">
        ID: <input type="number" name="id" required>
        Name: <input type="text" name="name" required>
        <input type="submit" value="Add">
    </form>

    <h2>Update User Name</h2>
    <form id="update-form">
        ID: <input type="number" name="id" required>
        New Name: <input type="text" name="name" required>
        <input type="submit" value="Update">
    </form>

    <h2>Delete User</h2>
    <form id="delete-form">
        ID: <input type="number" name="id" required>
        <input type="submit" value="Delete">
    </form>

<script>
// Fetch users and render table
function fetchUsers() {
    fetch('/api/users')
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector("#users-table tbody");
            tbody.innerHTML = "";
            data.rows.forEach(row => {
                const tr = document.createElement("tr");
                tr.innerHTML = `<td>${row.id}</td><td>${row.name}</td>`;
                tbody.appendChild(tr);
            });
        });
}

// Show messages for 3 seconds
function showMessage(msg) {
    const el = document.getElementById("message");
    el.textContent = msg;
    setTimeout(() => el.textContent = "", 3000);
}

// Add user
document.getElementById("add-form").addEventListener("submit", e => {
    e.preventDefault();
    const data = new FormData(e.target);
    fetch("/api/add", { method: "POST", body: data })
        .then(res => res.json())
        .then(r => { showMessage(r.message); fetchUsers(); e.target.reset(); });
});

// Update user
document.getElementById("update-form").addEventListener("submit", e => {
    e.preventDefault();
    const data = new FormData(e.target);
    fetch("/api/update", { method: "POST", body: data })
        .then(res => res.json())
        .then(r => { showMessage(r.message); fetchUsers(); e.target.reset(); });
});

// Delete user
document.getElementById("delete-form").addEventListener("submit", e => {
    e.preventDefault();
    const data = new FormData(e.target);
    fetch("/api/delete", { method: "POST", body: data })
        .then(res => res.json())
        .then(r => { showMessage(r.message); fetchUsers(); e.target.reset(); });
});

// Initial table load
fetchUsers();
</script>
</body>
</html>
"""

# --- Flask routes ---
@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/users")
def api_users():
    table = db.get_table("users")
    return jsonify({"rows": table.select()})

@app.route("/api/add", methods=["POST"])
def api_add():
    table = db.get_table("users")
    id_val = int(request.form["id"])
    name = request.form["name"]
    try:
        table.insert([id_val, name])
        msg = f"User {name} added successfully."
    except ValueError:
        msg = f"Error: User with ID {id_val} already exists."
    return jsonify({"message": msg})

@app.route("/api/update", methods=["POST"])
def api_update():
    table = db.get_table("users")
    id_val = int(request.form["id"])
    name = request.form["name"]
    count = table.update(("id", id_val), {"name": name})
    msg = f"{count} row(s) updated." if count else f"No user found with ID {id_val}."
    return jsonify({"message": msg})

@app.route("/api/delete", methods=["POST"])
def api_delete():
    table = db.get_table("users")
    id_val = int(request.form["id"])
    count = table.delete(("id", id_val))
    msg = f"{count} row(s) deleted." if count else f"No user found with ID {id_val}."
    return jsonify({"message": msg})

if __name__ == "__main__":
    app.run(debug=True)
