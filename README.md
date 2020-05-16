# Export Google Playlists

Google Music is awesome, and so google is going to kill it off. 

So, if you're like me and have lots of carefully curated playlists generated over the years, this is not happy news. Yes, in theory, these will be moved over to Youtube Music, but let's be honest, you're here. If this wasn't a sore point, you wouldn't be.

So I wrote a quick, crappy script to either dump the playlist into a csv, or import them directly into Spotify. 

## To get your playlist out of Google Music

This one is going to be annoying, but basically:

1. go to your playlist page.
2. Open the developer tools for the browser of your choice. 
3. Look in the "Network" tab. 
4. Force refresh the page, then look for the `loaduserplaylist` call. 
5. Dump the raw json into a file named: "`your_playlist`.json" (where `your_playlist` is whatever name you originally gave it.)

## Running the scripts

These are python scripts, so yeah, you want to probably run in a virtualenv and you want to 
`pip install -r requirements.txt`

### Dumping to a CSV

to_csv.py just reads the .json file you give it and creates a simple CSV containing the artist, title, album and a link to the cover art if it's there. Feel free to go nuts and add OPML or whatever support. I don't need it, but this was more a proof of concept.

### Dumping to Spotify

This one takes a few extra steps.

You'll need to get a developer key from [the Spotify API](https://developer.spotify.com/dashboard/applications). You will probably need to create an app. It can be desktop, and be sure to give it a Redirect URL (like `http://localhost` or something. You'll need that later.)

Then set the following Environment Variables:

```
SPOTIPY_CLIENT_ID=[Your Client ID] \
SPOTIPY_CLIENT_SECRET=[Your Client Secret] \
SPOTIPY_USER=[Your Spotipy Username] \
```

You can even be super clever and create a `run.sh` script that sets those vars for you like

```
#!/bin/bash
SPOTIPY_CLIENT_ID=abc123 \
SPOTIPY_CLIENT_SECRET=fake456 \
SPOTIPY_USER=joerandom \
venv/bin/python to_spotipy.py $*
```

But, I'm not your Dad.

If you give to_spotify a `playlist` name, it will look for `playlist.json` and create a new spotify playlist called `playlist`. Any titles it can't match up will go into a fille called `not_found.csv` which will have the track title and artist, and if there was a close match in Spotify, it will show the search string. If the script screwed up, you can use that to find the title and add it yourself. 

Whaddya want for nothin'?
