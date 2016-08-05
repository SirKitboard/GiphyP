from flask import Flask, request, jsonify
import requests
from os.path import join, dirname
from dotenv import load_dotenv
from flask.ext.api import status
import json

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

app = Flask(__name__)

user_state_dict = {

}

@app.route("/", methods=["POST"])
def hello():
    if(request.form["token"] != SLACK_TOKEN):
        return status.HTTP_401_UNAUTHORIZED

    username = request.form['user_name']
    if username not in user_state_dict:
        user_state_dict[username] = {
            "state": 0,
            "offset": 0,
        }

    if(user_state_dict[username][state] == 0):
        results = returnSearch(0, request.form["text"], username)
        responseDict = {"attachments": []}
        for link in results:
            responseDict["attachments"].append({"image_url": link})

        return jsonify(**responseDict)

    elif(user_state_dict[username][state] == 1):
        if(isInt(request.form["text"]) and int(request.form["text"]) < 4 and int(request.form["text"]) > 0):
            responseDict = {"attachments": [{"image_url":user_state_dict[username]["last_results"][int(request.form["text"])]}]}
            responseDict["response_type"] = "in_channel"
            return jsonify(**responseDict)

    return status.HTTP_404_NOT_FOUND

def isInt(value):
  try:
    int(value)
    return True
  except:
    return False

def returnSearch(offset, query, username):
    params = {
        "limit":3,
        "offset": offset,
        "q": query,
        "api_key":"dc6zaTOxFJmzC"
    }

    r = requests.get("http://api.giphy.com/v1/gifs/search", params=payload)
    links = []
    for data in json.loads(r.text)["data"]:
        links.append[data["url"]]

    user_state_dict[username]["state"] = 1
    user_state_dict[username]["last_results"] = links
    user_state_dict[username]["last_query"] = request.form["text"]
    user_state_dict[offset]["offset"] = offset + 3

    return links


if __name__ == "__main__":
    app.run(threaded=True)
