# Spotify To Youtube
Import all the songs in a Spotify playlist to a Youtube playlist.
Tested on Mac OS 12.16.3 with Python 3.9.16.

# Getting Started
1. Install dependencies
> pip install -r requirements.txt 
2. Make sure your YT account is a channel

## Configure Google Cloud to support this app
1. Login to the Google account in which you want to import your songs
1. Navigate to https://console.cloud.google.com
1. Create a new project and name it ‘SF2YT’ or any other name
1. Search for ‘youtube data api v3’ and click on ‘enable’
1. After you’re forwarded to the ‘API & Services’ dashboard, click
on credentials > API Key to create an API key
1. Click on ‘Create Credentials’ > ‘OAUTH Client ID’ 
   1. Select ‘Desktop App’ and name it anything you want
   1. Select user type 'External' (this is probably the only option available)
   1. Fill in the app information using common sense
   1. Skip the screen for 'scopes'
   1. Add the e-mail address for the YT account to 'test users'
1. Download the JSON with the credentials to the root of this project and rename it to ‘youtube_client_id_secret.json’

## Configure Spotify API to support this app
1. Navigate to https://developer.spotify.com/dashboard
2. Press ‘create app’
3. Fill in the required fields and in the field redirect URL
‘http://localhost:8888/redirect’
4. Go to ‘Settings’ and copy the client_id and client_secret
5. In the root of the project create a file called ‘spotify_client_id_secret.json’ and paste the following JSON object

>{
"client_id":
"",
"client_secret"
:
""
}

6. Fill in the client_id and client_secret fields and save.

## Run the application
1. Run main.py, click on the link in the terminal
2. Add the ‘authorization code’ to the terminal

# To do (for further development):
- User selection of spotify playlist by name instead of ID
- Add music information to the YT playlist notes
- Fix OAUTH redirect so that the access key doesn't need to be copied by the user
- Run in Docker container to support cross platform