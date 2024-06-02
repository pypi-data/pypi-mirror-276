"""upstox login"""
import urllib.parse
import requests

def login(apikey,secretkey,rurl):
    """ Fuction to acquire an access token via an authorization_code exchange
    Args:
        apikey (str): Upstox Api key
        secretkey (str): Upstox Api secret code
        rurl (str): Redirect uri

    Returns:
        str: Access token
    """
    rurl_parsed=urllib.parse.quote(rurl,safe="")
    uri=f'https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={apikey}&redirect_uri={rurl_parsed}'
    print("Visit the following URL to authorize your application:")
    print(uri)
    code = input("Enter the code: ")
    url=f"https://api.upstox.com/v2/login/authorization/token"
    headers={'accept': "application/json",'Content-Type': "application/x-www-form-urlencoded"}
    data={'code':code,'client_id':apikey,'client_secret':secretkey,'redirect_uri':rurl,'grant_type':'authorization_code'}
    response=requests.post(url,headers=headers,data=data)
    json_response=response.json()
    access_token=json_response['access_token']
    print('access token created')
    return access_token