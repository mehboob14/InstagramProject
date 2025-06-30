import http.server
import datetime
import socketserver
import threading
import subprocess
import time
import json
import requests

PORT = 8001
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
thread = threading.Thread(target=httpd.serve_forever)
thread.start()

ngork = subprocess.Popen([r"C:\Users\Administrator\Desktop\Instagram_Project\Starting\ngrok.exe", "http", str(PORT)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(2)

resp = requests.get("http://localhost:4040/api/tunnels")
public_url = json.loads(resp.text)["tunnels"][0]["public_url"]
print(f"Public URL: {public_url}")
image_url = f"{public_url}/post.jpg"
print(f"Image URL: {image_url}")


caption  = "Success is not in Never Falling, but in Rising Every Time We Fall. #Motivation #Inspiration #Success"


ig_user_id = "17841475639279338"
access_token = "EAAa6YbICp40BOzXyFxWDZBCmrUbT9DFjIpzUz8wlu2qVRwsRorqs3jzwvZBa7r7nYUQVFRP5DYKH0PjZAJ3zz7wtSgq2qEZAkN2hgrgTomx7Apjd8TaYZCLKZAcCFj48mt1OVcZBtzxlbOa2aLykyEb0JsEFi2lyPlZC3y2oiNMdIx8lSJ4MICmjuVJMZAW56NykaRpam1Bdc"
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
    # "media_type" : "STORIES",
    "collaborators": json.dumps(["mountainbetweenus"]),
    "access_token": access_token
}


response = requests.post(url, data=payload)
data = response.json()
print(json.dumps(data, indent=4))
create_id = data.get("id")
print(f"Creation ID: {create_id}")

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



# url  = "https://graph.facebook.com/v23.0/{media_id}"

# payload = {
#     "fields": "comments_count,like_count,thumbnail_url,permalink,timestamp",
#     "access_token": access_token
# }

# res = requests.get(url, params=payload)
# data = res.json()
# print(json.dumps(data, indent=4))

# httpd.shutdown()
# httpd.server_close()
