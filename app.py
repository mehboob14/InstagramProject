import json
import requests

# ✅ Static public URL for your Flask app on Render
public_url = "https://instagramproject-4.onrender.com"
image_url = f"{public_url}/static/post.jpg"
print(f"Image URL: {image_url}")

caption = "Success is not in Never Falling, but in Rising Every Time We Fall. #Motivation #Inspiration #Success"

ig_user_id = "YOUR_IG_USER_ID"
access_token = "YOUR_ACCESS_TOKEN"  # ideally use the one you get via OAuth flow

# ✅ 1. Create media container
url = f"https://graph.facebook.com/v23.0/{ig_user_id}/media"

payload = {
    "image_url": image_url,
    "caption": caption,
    "user_tags": json.dumps([
        {
            "username": "bluebottle",
            "x": 0.5,
            "y": 0.5
        }
    ]),
    "collaborators": json.dumps(["mountainbetweenus"]),
    "access_token": access_token
}

response = requests.post(url, data=payload)
data = response.json()
print(json.dumps(data, indent=4))

create_id = data.get("id")
print(f"Creation ID: {create_id}")

# ✅ 2. Publish the media
url = f"https://graph.facebook.com/v23.0/{ig_user_id}/media_publish"

payload = {
    "creation_id": create_id,
    "access_token": access_token
}

response = requests.post(url, params=payload)
data = response.json()
print(json.dumps(data, indent=4))

if "id" in data:
    print(f"Post published successfully. Media ID: {data['id']}")

media_id = data.get("id")
print(f"Media ID: {media_id}")
