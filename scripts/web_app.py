from flask import Flask, render_template, request, redirect, url_for, jsonify
from .command_handler import run_command
from .db_handler import get_all_targets, init_db, get_targets_version

HISTORY_MAX_LEN = 10

app = Flask(__name__)

history = []

init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        command = request.form.get("command", "")

        result = run_command(command=command)

        history.append(result)
        if len(history) > HISTORY_MAX_LEN:
            history.pop(0)

        return redirect(url_for("home"))

    return render_template(
        "index.html",
        targets=get_all_targets(),
        history=history
    )

@app.route("/api/targets-version")
def targets_version():
    return jsonify({"version": get_targets_version()})

if __name__ == "__main__":
    app.run(debug=True, port=5050)