from flask import Flask, render_template, request
from command_handler import run_command

HISTORY_MAX_LEN = 5

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

        return render_template(
            "index.html",
            message=result["message"],
            ok=result["ok"],
            command=command,
            targets=result["targets"],
            history=history
        )

    return render_template(
        "index.html",
        message="",
        ok=True,
        command="",
        targets={},
        history=[]
    )

if __name__ == "__main__":
    app.run(debug=True, port=5050)