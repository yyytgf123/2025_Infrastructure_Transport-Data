from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    budget = request.args.get("budget", default=100000, type=int)
    area = request.args.get("area", default=60, type=float)
    work_address = request.args.get("work_address", default="서울특별시 중구 세종대로 110", type=str)
    use_radius = 'use_radius' in request.args
    return render_template("index.html", budget=budget, area=area, work_address=work_address, use_radius=use_radius)


def map():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)