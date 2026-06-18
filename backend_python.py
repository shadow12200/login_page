from flask import Flask,request,jsonify
import mysql.connector as m 

app = Flask(__name__, static_folder="static")
passwd='SUDOssy@26'
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



@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    result = check_credentials(username, password)
    if result:
        return jsonify({
            "success": True,
            "message": "Login successful"
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        })

if __name__ == "__main__":
    app.run(debug=True)