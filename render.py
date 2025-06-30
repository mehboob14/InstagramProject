from flask import Flask, jsonify

import json
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return "Your Instagram Project Home"

@app.route("/post_to_instagram")
def post_to_instagram():
    # ✅ Use your Render domain for public_url
    public_url = "https://instagramproject-4.onrender.com"
    image_url = f"{public_url}/static/post.jpg"

    caption = "Success is not in Never Falling, but in Rising Every Time We Fall. #Motivation #Inspiration #Success"

    ig_user_id = "YOUR_IG_USER_ID"
    access_token = "YOUR_ACCESS_TOKEN"

    # ✅ 1. Create media
    url = f"https://graph.facebook.com/v23.0/{ig_user_id}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "user_tags": json.dumps([{"username": "bluebottle", "x": 0.5, "y": 0.5}]),
        "collaborators": json.dumps(["mountainbetweenus"]),
        "access_token": access_token
    }

    response = requests.post(url, data=payload)
    data = response.json()
    print(json.dumps(data, indent=4))
    create_id = data.get("id")

    # ✅ 2. Publish media
    publish_url = f"https://graph.facebook.com/v23.0/{ig_user_id}/media_publish"
    publish_payload = {
        "creation_id": create_id,
        "access_token": access_token
    }

    response = requests.post(publish_url, params=publish_payload)
    publish_data = response.json()
    print(json.dumps(publish_data, indent=4))

    return jsonify({
        "create_id": create_id,
        "publish_response": publish_data
    })
