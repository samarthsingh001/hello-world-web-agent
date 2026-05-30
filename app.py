from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello, World!</h1><p>My first web agent is live.</p>"

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)
