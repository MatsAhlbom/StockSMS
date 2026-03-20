from flask import Flask, render_template, request, redirect, url_for
from command_handler import run_command, load_targets

HISTORY_MAX_LEN = 10

app = Flask(__name__)

history = []

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
        targets=load_targets(),
        history=history
    )

if __name__ == "__main__":
    app.run(debug=True, port=5050)