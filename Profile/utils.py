import requests
import base64
from django.conf import settings

def get_zoom_tokens(grant_type,token,redirect_uri):
    username = settings.ZOOM_CLIENT_ID
    password = settings.ZOOM_CLIENT_SECRET
    
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    payload={
        "code": token,
        "grant_type": grant_type, # authorization_code for getting refresh token and refresh_token for getting access token
        "redirect_uri": redirect_uri
    }
    
    response = requests.request("POST", settings.ZOOM_ACCESS_TOKEN_OBTAIN_URL, headers=headers, data=payload)
    return response.json()['access_token'], response.json()['refresh_token'] 
    