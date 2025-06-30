import requests
import json


url = "https://graph.facebook.com/v23.0/17841475639279338/?fields=business_discovery.username(bluebottle){followers_count,media_count}&access_token=EAAa6YbICp40BO7apiBnV4LbTHq3xcAcHoZBtZA5poRgVT8bcFPpcuZAvWmIfb36zBqQOuRODBij36CaI8YMqW762s0VcsmxoPyCS4leDhlH724nx67Mbx3WKAC8J4wUM6Wp5f7VTAQU7RqNZB2okakHTW98zo6d0Sy7mGwj0s8gapEQ1NZA7I86da9Amrvqro"

response = requests.get(url)
print(response.status_code)
print(response.text)
if response.status_code == 200:
    metadata = response.json()
    followers = metadata["business_discovery"]["followers_count"]
    media_count = metadata["business_discovery"]["media_count"]
    print(f"Followers: {followers}, Media Count: {media_count}")