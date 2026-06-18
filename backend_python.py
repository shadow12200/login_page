from flask import Flask,request,jsonify

app = Flask(__name__, static_folder="static")

@app.route("/")
def home():
    return app.send_static_file("log_in.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    print(f"Username: {username}")
    print(f"Password: {password}")

    return jsonify({
        "success": True,
        "message": "Data received"
    })

if __name__ == "__main__":
    app.run(debug=True)