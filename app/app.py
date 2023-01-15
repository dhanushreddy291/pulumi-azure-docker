from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "A Dockerized Flask app created using Pulumi on Azure 😎"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)