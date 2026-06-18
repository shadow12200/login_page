from flask import Flask,request,jsonify
import mysql.connector as m 
import secrets


app = Flask(__name__, static_folder="static")
passwd='check123'
db='login_system'
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
    query="INSERT INTO sessions (session_token, username) VALUES (%s, %s)"
    cursor.execute(query, (token, username))
    con.commit()
    cursor.close()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    result = check_credentials(username, password)
    if result:
        token = secrets.token_hex(32)

        response = jsonify({
            "success": True,
            "message": "Login successful"
        })
        response.set_cookie("auth_token", 
                           token, 
                           httponly=True, 
                           secure=False,
                           samesite='Lax')
        return response
        
    else:
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        })
    


if __name__ == "__main__":
    app.run(debug=True)