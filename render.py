from flask import Flask, render_template, redirect, url_for, session, request, jsonify
import os
import json
import requests

app = Flask(__name__)
app.secret_key = "testsecretkey"


FB_APP_ID = "1893778621376397"
FB_APP_SECRET = "9ad13d22e80ac416f8d60e97f995de2c"
FB_REDIRECT_URI = "https://instagramproject-4.onrender.com/callback/facebook"
FB_SCOPE = "pages_show_list,instagram_basic,instagram_content_publish"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login/facebook")
def login_facebook():
    auth_url = (
        f"https://www.facebook.com/v23.0/dialog/oauth"
        f"?client_id={FB_APP_ID}"
        f"&redirect_uri={FB_REDIRECT_URI}"
        f"&scope={FB_SCOPE}"
        f"&response_type=code"
    )
    return redirect(auth_url)

@app.route("/callback/facebook")
def callback_facebook():
    code = request.args.get("code")


    token_url = "https://graph.facebook.com/v23.0/oauth/access_token"
    params = {
        "client_id": FB_APP_ID,
        "redirect_uri": FB_REDIRECT_URI,
        "client_secret": FB_APP_SECRET,
        "code": code,
    }

    token_response = requests.get(token_url, params=params)
    data = token_response.json()
    access_token = data.get("access_token")
    print("Access Token Response:", json.dumps(data, indent=4))

    if not access_token:
        return "Failed to get access token"

    session["access_token"] = access_token


    pages_url = "https://graph.facebook.com/v23.0/me/accounts"
    pages_params = {
        "access_token": access_token
    }
    pages_response = requests.get(pages_url, params=pages_params)
    pages_data = pages_response.json()
    print("Pages Data:", json.dumps(pages_data, indent=4))

    pages = pages_data.get("data", [])
    if not pages:
        return "No Facebook Pages found for this user."

    page_id = pages[0]["id"]
    print(f"Page ID: {page_id}")

    ig_url = f"https://graph.facebook.com/v23.0/{page_id}"
    ig_params = {
        "fields": "instagram_business_account",
        "access_token": access_token
    }
    ig_response = requests.get(ig_url, params=ig_params)
    ig_data = ig_response.json()
    print("IG Data:", json.dumps(ig_data, indent=4))

    instagram_account = ig_data.get("instagram_business_account")
    if not instagram_account:
        return "No Instagram Business Account connected to this Page."

    ig_user_id = instagram_account["id"]
    print(f"Dynamic IG_USER_ID: {ig_user_id}")


    session["ig_user_id"] = ig_user_id

    return redirect(url_for("dashboard"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "access_token" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        uploaded_file = request.files["image"]
        if uploaded_file.filename != "":
            image_path = os.path.join("static", "post.jpg")
            uploaded_file.save(image_path)

        caption = request.form.get("caption", "")
        session["caption"] = caption

        return redirect(url_for("post_to_instagram"))

    return render_template("dashboard.html")

@app.route("/post_to_instagram")
def post_to_instagram():
    access_token = session.get("access_token")
    caption = session.get("caption", "")
    ig_user_id = session.get("ig_user_id")

    if not access_token:
        return "No access token found. Please authenticate first."
    if not ig_user_id:
        return "No Instagram Business Account ID found. Please authenticate again."

    public_url = "https://instagramproject-4.onrender.com"
    image_url = f"{public_url}/static/post.jpg"


    url = f"https://graph.facebook.com/v23.0/{ig_user_id}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }

    response = requests.post(url, data=payload)
    data = response.json()
    print("Create Media:", json.dumps(data, indent=4))
    creation_id = data.get("id")

    if not creation_id:
        return f"Failed to create media: {data}"


    publish_url = f"https://graph.facebook.com/v23.0/{ig_user_id}/media_publish"
    publish_payload = {
        "creation_id": creation_id,
        "access_token": access_token
    }

    publish_response = requests.post(publish_url, params=publish_payload)
    publish_data = publish_response.json()
    print("Publish Response:", json.dumps(publish_data, indent=4))

    return jsonify({
        "creation_id": creation_id,
        "publish_response": publish_data
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
