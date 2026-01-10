from flask import Flask, request, jsonify
from rdbms.database import Database

app = Flask(__name__)
db = Database()

db.create_table("users", ["id", "email", "name"], primary_key="id", unique_keys=["email"])

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    db.get_table("users").insert([data["id"], data["email"], data["name"]])
    return jsonify({"message": "User created"})

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(db.get_table("users").select())

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    db.get_table("users").update(("id", user_id), data)
    return jsonify({"message": "User updated"})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db.get_table("users").delete(("id", user_id))
    return jsonify({"message": "User deleted"})

if __name__ == "__main__":
    app.run(debug=True)
