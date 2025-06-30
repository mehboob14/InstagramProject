import requests
import json
import os
import urllib.request
import ssl
import certifi

# sll_context = ssl.create_default_context(cafile=certifi.where())

# os.environ['SLL_CERT_FILE'] = certifi.where()
# # url = "https://graph.facebook.com/v23.0/17841475639279338/?fields=business_discovery.username(bluebottle){followers_count,media_count}&access_token=EAAa6YbICp40BO7apiBnV4LbTHq3xcAcHoZBtZA5poRgVT8bcFPpcuZAvWmIfb36zBqQOuRODBij36CaI8YMqW762s0VcsmxoPyCS4leDhlH724nx67Mbx3WKAC8J4wUM6Wp5f7VTAQU7RqNZB2okakHTW98zo6d0Sy7mGwj0s8gapEQ1NZA7I86da9Amrvqro"
# #url = "https://google.com"
url = "https://graph.facebook.com"

response = urllib.request.urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
print(response.status_code)

# url = "https://www.google.com"
# respnose = urllib.request.urlopen(url, context=sll_context)
# print(respnose.status)

# import requests
# requests.get(url, verify='/path/to/cacert.pem')

# import platform
# # ...

# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
# ssl_context.verify_mode = ssl.CERT_REQUIRED
# ssl_context.check_hostname = True
# ssl_context.load_default_certs()

# if platform.system().lower() == 'darwin':
#     import certifi
#     ssl_context.load_verify_locations(
#         cafile=os.path.relpath(certifi.where()),
#         capath=None,
#         cadata=None)
    
# import urllib
# # previous context
# https_handler = urllib.request.HTTPSHandler(context=ssl_context)

# opener = urllib.request.build_opener(https_handler)
# ret = opener.open(url, timeout=2)