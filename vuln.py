import os
import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

# 1. Hardcoded secret
API_KEY = "1234567890abcdef"

# 2. SQL Injection vulnerability
@app.route("/user")
def get_user():
    username = request.args.get("username")
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return {"result": result}

# 3. Command Injection vulnerability Test
@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    command = f"ping -c 4 {ip}"
    output = subprocess.check_output(command, shell=True)
    return {"output": output.decode()}

# 4. Insecure deserialization
@app.route("/load")
def load_object():
    import pickle
    data = request.args.get("data")
    obj = pickle.loads(bytes.fromhex(data))
    return {"object": str(obj)}

# 5. Insecure file write
@app.route("/write")
def write_file():
    filename = request.args.get("filename")
    content = request.args.get("content")
    with open(f"/tmp/{filename}", "w") as f:
        f.write(content)
    return {"status": "written"}

# 6. Missing authentication
@app.route("/admin")
def admin_panel():
    return {"status": "admin access granted"}

if __name__ == "__main__":
    app.run(debug=True)
