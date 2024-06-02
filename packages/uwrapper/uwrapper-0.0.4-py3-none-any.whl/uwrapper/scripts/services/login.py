"""upstox login"""
from ...config.config import get_configs
import urllib.parse
import requests

def login(apikey,secretkey,rurl):
    """ logging into upstox """
    config=get_configs()
    rurl_parsed=urllib.parse.quote(rurl,safe="")
    uri=f'{config["login_url"]}=code&client_id={apikey}&redirect_uri={rurl_parsed}'
    print("Visit the following URL to authorize your application:")
    print(uri)
    code = input("Enter the code: ")
    url=f"{config['authorization_token_url']}"
    headers={'accept': "application/json",'Content-Type': "application/x-www-form-urlencoded"}
    data={'code':code,'client_id':apikey,'client_secret':secretkey,'redirect_uri':rurl,'grant_type':'authorization_code'}
    response=requests.post(url,headers=headers,data=data)
    json_response=response.json()
    access_token=json_response['access_token']
    print('access token created')
    return access_token