from flask import Flask, redirect, request, jsonify
import requests

app = Flask(__name__)


APP_ID = '1893778621376397'
APP_SECRET = '9ad13d22e80ac416f8d60e97f995de2c'
REDIRECT_URI = 'https://84b7-58-27-202-194.ngrok-free.app/callback'
LONG_LIVED_ACCESS_TOKEN = 'EAAa6YbICp40BO7apiBnV4LbTHq3xcAcHoZBtZA5poRgVT8bcFPpcuZAvWmIfb36zBqQOuRODBij36CaI8YMqW762s0VcsmxoPyCS4leDhlH724nx67Mbx3WKAC8J4wUM6Wp5f7VTAQU7RqNZB2okakHTW98zo6d0Sy7mGwj0s8gapEQ1NZA7I86da9Amrvqro'



@app.route('/')
def home():
    return '<a href="/login">Login with Facebook</a>'


@app.route('/login')
def login():
    fb_auth_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth?"
        f"client_id={APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=pages_show_list,instagram_basic,instagram_content_publish,pages_read_engagement"
        f"&response_type=code"
    )
    return redirect(fb_auth_url)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'No code provided by Facebook.'

    token_url = 'https://graph.facebook.com/v18.0/oauth/access_token'
    params = {
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    }

    r = requests.get(token_url, params=params)
    data = r.json()
    return jsonify(data)


@app.route('/me')
def me():
    """Get Facebook user info using long-lived token"""
    url = 'https://graph.facebook.com/v18.0/me'
    params = {
        'access_token': LONG_LIVED_ACCESS_TOKEN,
        'fields': 'id,name'
    }
    r = requests.get(url, params=params)
    return jsonify(r.json())


@app.route('/post')
def post():
    """Post an image to Instagram via connected Page"""
    
    
    pages_url = 'https://graph.facebook.com/v18.0/me/accounts'
    pages = requests.get(pages_url, params={'access_token': LONG_LIVED_ACCESS_TOKEN}).json()
    page_id = pages['data'][0]['id']
    page_token = pages['data'][0]['access_token']

    
    ig_url = f'https://graph.facebook.com/v18.0/{page_id}?fields=instagram_business_account'
    ig_data = requests.get(ig_url, params={'access_token': page_token}).json()
    ig_user_id = ig_data['instagram_business_account']['id']

    
    image_url = 'https://i.imgur.com/BoN9kdC.png'  
    caption = 'Hello from Flask!'
    media_url = f'https://graph.facebook.com/v18.0/{ig_user_id}/media'
    media_params = {
        'image_url': image_url,
        'caption': caption,
        'access_token': page_token
    }
    media_res = requests.post(media_url, data=media_params).json()
    creation_id = media_res.get('id')

    if not creation_id:
        return jsonify(media_res)

 
    publish_url = f'https://graph.facebook.com/v18.0/{ig_user_id}/media_publish'
    publish_res = requests.post(publish_url, data={
        'creation_id': creation_id,
        'access_token': page_token
    }).json()

    return jsonify({
        'status': 'Post Published!',
        'creation_id': creation_id,
        'publish_response': publish_res
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
