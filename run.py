from vitahistory import create_app
from flask import redirect, url_for

app = create_app()

@app.route("/")
def redirection():
    return redirect(url_for('index.home'))


if __name__ == "__main__":
    app.run(debug=True)
