from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def map():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)