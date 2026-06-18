from flask import Flask

app = Flask(__name__, static_folder="static")

@app.route("/")
def home():
    return app.send_static_file("log_in.html")

if __name__ == "__main__":
    app.run(debug=True)