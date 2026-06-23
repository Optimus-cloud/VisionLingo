from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# TEMP database (replace later with real DB)
users = []

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data["email"]
    password = data["password"]

    # Check if user exists
    for user in users:
        if user["email"] == email:
            return jsonify({"message": "User already exists"}), 400

    users.append({"email": email, "password": password})

    return jsonify({"message": "Signup successful"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({"message": "Login success"})

    return jsonify({"message": "Invalid credentials"}), 401


if __name__ == "__main__":
    app.run(debug=True)