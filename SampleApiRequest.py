from flask import Flask
import requests
from urllib.parse import urlparse, parse_qs
import time
from selenium import webdriver
from pprint import pprint
import json

#
# files = {
#     'client_id': (None, 'CLIENT_ID'),
#     'client_secret': (None, 'CLIENT_SECRET'),
#     'grant_type': (None, 'authorization_code'),
#     'redirect_uri': (None, 'AUTHORIZATION_REDIRECT_URI'),
#     'code': (None, 'CODE'),
# }
#
# response = requests.post('https://api.instagram.com/oauth/access_token', files=files)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    #r = requests.get('https://api.instagram.com/oauth/authorize/?client_id=aaf3d7ca2ac643e58733bf35d1535f5e&redirect_uri=http://localhost:3000&response_type=code')

    #driver = webdriver.Chrome(executable_path='C:/Users/Andrew/Downloads/chromedriver.exe')

    driver = webdriver.Chrome(r'C:/Users/Andrew/Downloads/chromedriver.exe')

    driver.get('https://api.instagram.com/oauth/authorize/?client_id=aaf3d7ca2ac643e58733bf35d1535f5e&redirect_uri=http://localhost:3000&response_type=code')

    time.sleep(30)
    URL = driver.current_url

    parsed_url = urlparse(URL)
    h = parse_qs(parsed_url.query)
    pprint(h['code'])
    driver.close()


    files = {
         'client_id': (None, 'aaf3d7ca2ac643e58733bf35d1535f5e'),
         'client_secret': (None, '762c26b0c23b4cbfb302c88a20500e9c'),
         'grant_type': (None, 'authorization_code'),
         'redirect_uri': (None, 'http://localhost:3000'),
         'code': (None, h['code'][0]),
         }
    request = requests.post('https://api.instagram.com/oauth/access_token', files=files)

    print(request.status_code)

    p = request.json()

    pprint(p)

    request1 = requests.get('https://api.instagram.com/v1/users/self/?access_token='+p['access_token'])

    p1 = request1.json()
    p11 = str(p1)
    pprint(p1)

    request2 = requests.get('https://api.instagram.com/v1/users/self/media/recent/?access_token='+p['access_token'])

    p2 = request2.json()
    p22 = str(p2)

    with open('reponse_ig.txt', 'w', encoding='utf-8') as f:
        # f.write(p11)
        # f.write('\n')
        # f.write(p22)
        # f.close()
        print(json.dumps(p1, sort_keys=True, indent=4, ensure_ascii=False), file=f)
        print(json.dumps(p2, sort_keys=True, indent=4, ensure_ascii=False), file=f)

    pprint(p2)
    return 'hello'

if __name__ == '__main__':
    app.run()
