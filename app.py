from flask import Flask, request, jsonify
import requests
from os.path import join, dirname
from flask.ext.api import status
import json

import os
from dotenv import Dotenv
dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env")) # Of course, replace by your correct path
os.environ.update(dotenv)

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

    if(user_state_dict[username]["state"] == 0):
        results = returnSearch(0, request.form["text"], username)
        responseDict = {"attachments": []}
        for link in results:
            responseDict["attachments"].append({"image_url": link, "text": "Gif"})
        responseDict["text"] = "Response"

        return jsonify(**responseDict)

    elif(user_state_dict[username]["state"] == 1):
        if(isInt(request.form["text"]) and int(request.form["text"]) < 4 and int(request.form["text"]) > 0):
            responseDict = {"attachments": [{"text":" ", "image_url":user_state_dict[username]["last_results"][int(request.form["text"])]}]}
            responseDict["response_type"] = "in_channel"
            responseDict["text"] = "@"+username+": "+ user_state_dict[username]["last_query"]
            print responseDict
            return jsonify(**responseDict)

    return status.HTTP_404_NOT_FOUND

def isInt(value):
  try:
    int(value)
    return True
  except:
    return False

def returnSearch(offset, query, username):
    payload = {
        "limit":3,
        "offset": offset,
        "q": query,
        "api_key":"dc6zaTOxFJmzC"
    }

    r = requests.get("http://api.giphy.com/v1/gifs/search", params=payload)
    links = []
    data = r.json()
    #data["data"]
    for giphy in data["data"]:
        print(giphy)
       # dadict = json.loads(giphy)
        links.append(giphy['images']['fixed_height']['url'])

    user_state_dict[username]["state"] = 1
    user_state_dict[username]["last_results"] = links
    user_state_dict[username]["last_query"] = request.form["text"]
    user_state_dict[username]["offset"] = offset + 3

    return links


if __name__ == "__main__":
    app.run()
