from flask import Flask, request, jsonify
import sqlite3
import os
import hashlib

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "users.db")

@app.route("/")
def home():
    return jsonify({"message": "Parent Portal Running", "version": "1.0"})

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # INTENTIONAL OWASP A03 — SQL injection for SonarQube to find
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        # INTENTIONAL OWASP A02 — password logged in plaintext
        print(f"User logged in: {username} with password {password}")
        return jsonify({"status": "success"})
    return jsonify({"status": "failed"}), 401

@app.route("/user", methods=["GET"])
def get_user():
    # INTENTIONAL OWASP A01 — no authentication check
    user_id = request.args.get("id")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
    row = cursor.fetchone()
    conn.close()
    return jsonify({"user": row})

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # INTENTIONAL OWASP A05 — debug mode on in production
    app.run(host="0.0.0.0", port=5000, debug=True)
