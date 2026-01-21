from flask import Flask, render_template, request, send_file
from Scanner.system_scan import system_scan
from Scanner.network_scan import network_scan
from Scanner.file_scan import file_scan
from Scanner.report import save_json

app = Flask(__name__)

LAST_REPORT = None  # przechowuje ostatni raport w pamięci


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    global LAST_REPORT

    mode = request.form.get("mode")
    target = request.form.get("target", "").strip()
    path = request.form.get("path", "").strip()

    try:
        if mode == "system":
            result = system_scan()

        elif mode == "network":
            if not target:
                result = {"error": "Nie podano hosta do skanowania"}
            else:
                result = network_scan(target)

        elif mode == "files":
            if not path:
                result = {"error": "Nie podano ścieżki do skanowania"}
            else:
                result = file_scan(path)

        else:
            result = {"error": "Nieznany tryb skanowania"}

    except Exception as e:
        result = {
            "error": "Wystąpił błąd podczas skanowania",
            "details": str(e)
        }

    LAST_REPORT = result
    return render_template("report.html", data=result, mode=mode)


@app.route("/save", methods=["POST"])
def save_report():
    if not LAST_REPORT:
        return {"error": "Brak raportu do zapisania"}

    filename = save_json(LAST_REPORT, "security_report.json")
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
