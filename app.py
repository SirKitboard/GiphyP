from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=["POST"])
def hello():
    for key in request.form:
        print(key + " : " + str(request.form[key]))

    return "HELLO"

if __name__ == "__main__":
    app.run()
