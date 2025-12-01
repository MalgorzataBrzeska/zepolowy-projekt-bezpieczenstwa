from flask import Flask, render_template, request
from Scanner.system_scan import system_scan
from Scanner.network_scan import network_scan
from Scanner.file_scan import file_scan

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    mode = request.form.get("mode")
    target = request.form.get("target")
    path = request.form.get("path")

    if mode == "system":
        result = system_scan()
    elif mode == "network":
        result = network_scan(target)
    elif mode == "files":
        result = file_scan(path)
    else:
        result = {"error": "unknown mode"}

    return render_template("report.html", data=result)

if __name__ == "__main__":
    app.run(debug=True)