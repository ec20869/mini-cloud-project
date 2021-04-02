#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install spotipy


# In[2]:


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
cid = 'a1cd8432f38240b4b73d237a85f997ce'
secret = '97642d8c2295492cb5a7ce21c3218b51'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager
=
client_credentials_manager)


# In[5]:


import requests

CLIENT_ID = 'a1cd8432f38240b4b73d237a85f997ce'
CLIENT_SECRET = '97642d8c2295492cb5a7ce21c3218b51'


# In[7]:


AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': 'a1cd8432f38240b4b73d237a85f997ce',
    'client_secret': '97642d8c2295492cb5a7ce21c3218b51',
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']


# In[8]:


headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}


# In[9]:


# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# Track ID from the URI
track_id = '6y0igZArWVi6Iz0rj35c1Y'

# actual GET request with proper header
r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)


# In[10]:


r = r.json()
r


# In[12]:


artist_id = '36QJpDe2go2KgaRleHCDTp'

# pull all artists albums
r = requests.get(BASE_URL + 'artists/' + artist_id + '/albums', 
                 headers=headers, 
                 params={'include_groups': 'album', 'limit': 50})
d = r.json()


# In[13]:


for album in d['items']:
    print(album['name'], ' --- ', album['release_date'])


# In[14]:


data = []   # will hold all track info
albums = [] # to keep track of duplicates

# loop over albums and get all tracks
for album in d['items']:
    album_name = album['name']

    # here's a hacky way to skip over albums we've already grabbed
    trim_name = album_name.split('(')[0].strip()
    if trim_name.upper() in albums or int(album['release_date'][:4]) > 1983:
        continue
    albums.append(trim_name.upper()) # use upper() to standardize
    
    # this takes a few seconds so let's keep track of progress    
    print(album_name)
    
    # pull all tracks from this album
    r = requests.get(BASE_URL + 'albums/' + album['id'] + '/tracks', 
        headers=headers)
    tracks = r.json()['items']
    
    for track in tracks:
        # get audio features (key, liveness, danceability, ...)
        f = requests.get(BASE_URL + 'audio-features/' + track['id'], 
            headers=headers)
        f = f.json()
        
        # combine with album info
        f.update({
            'track_name': track['name'],
            'album_name': album_name,
            'short_album_name': trim_name,
            'release_date': album['release_date'],
            'album_id': album['id']
        })
        
        data.append(f)


# In[ ]:




