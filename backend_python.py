from urllib import response

from flask import Flask,request,jsonify,send_file
import mysql.connector as m 
import secrets
import os

app = Flask(__name__, static_folder="static")
passwd=os.getenv("password")
db=os.getenv("db")
protected_directory=os.getenv("protected_directory")


@app.route("/")
def home():
    return app.send_static_file("log_in.html")


def check_credentials(username, password):
    con=m.connect(host="localhost", user="root", password=passwd, database=db)
    cursor=con.cursor()
    query="SELECT * FROM main_login WHERE username=%s AND password_hash=%s"
    cursor.execute(query, (username, password))
    result=cursor.fetchone()
    cursor.close()
    con.close()
    return result

def post_session(username,token):
    con=m.connect(host="localhost", user="root", password=passwd, database=db)
    cursor=con.cursor()
    main_query='SELECT * FROM sessions WHERE username=%s'
    cursor.execute(main_query, (username,))
    existing_session = cursor.fetchone()
    if existing_session:#protyping fix not
        cursor.execute("delete from sessions where username=%s", (username,))
        con.commit()
        query="INSERT INTO sessions (session_token, username) VALUES (%s, %s)"
        cursor.execute(query, (token, username))
        con.commit()
        cursor.close()
    else:
        query="INSERT INTO sessions (session_token, username) VALUES (%s, %s)"
        cursor.execute(query, (token, username))
        con.commit()
        cursor.close()

@app.route("/login", methods=["POST"])
def login():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")
    if not username or not password:
        return jsonify({"error":"Username and password are required"}), 400
    if check_credentials(username, password):
        token=secrets.token_hex(16)
        post_session(username,token)
        response = jsonify({"message": "Login successful"})
        response.set_cookie(
        "auth_token",
        token,
        httponly=True,
        secure=False,      # True when using HTTPS
        samesite="Lax"
        )
        return response
    else:
        return jsonify({"error":"Invalid credentials"}), 401

@app.route("/protected", methods=["GET"])
def protected():
    token = request.cookies.get("auth_token")
    if not token:
        return jsonify({"error":"Authorization token is required"}), 401
    else:
        con=m.connect(host="localhost", user="root", password=passwd, database=db)
        cursor=con.cursor()
        query="SELECT * FROM sessions WHERE session_token=%s"
        cursor.execute(query, (token,))
        result=cursor.fetchone()
        cursor.close()
        con.close()
        if result:
            return send_file(protected_directory)
        else:
            return jsonify({"error":"Invalid session token"}), 401


if __name__=="__main__":
    app.run(debug=True)