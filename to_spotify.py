# python
import os
import re
import logging
import json

import argparse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from unidecode import unidecode
from tabulator import Stream

scope = 'playlist-modify-public'
user = os.environ.get("SPOTIPY_USER")

logger = logging.getLogger("list_import")
logging.basicConfig(level='INFO')
rep = re.compile("\(.+\)")
rec = re.compile(r"[\(\)\-\[\]\.\,\:\ \"\']+")
ret = re.compile(r"\b(&|and|the|of)\b")
res = re.compile(r" +")

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", default=user)
    parser.add_argument("playlist", default="test")
    parser.add_argument('--redir', default="http://localhost")
    return parser.parse_args()

def esc(word):
    if not word:
        word = ""
    word.replace('"', '\\"')
    word.replace('|','\\|')
    return word

def get_tracks(args, spotify, rej):
    ff = open("{}.json".format(args.playlist))
    data = json.load(ff)
    print("Artist|Title|Album|Cover Art")
    tracks = []
    tot = 0
    for record in data[1][0]:
        tot += 1
        (guid, title, cover, artist, album, *data) = record
        track = as_track(spotify, rej, artist, title, album)
        if track:
            tracks.append(track)
    return (tracks, tot)

def clean(string):
    return res.sub("", rec.sub("", rep.sub(" ", ret.sub(" ",unidecode(string.lower()))))).strip()

def as_track(spotify, rej, artist, title, album):
    term = "{} {}".format(artist, rep.sub("", title))
    logging.info("Searching {}".format(term))
    result = spotify.search(term)
    try:
        if result is None or len(result["tracks"]["items"]) == 0:
            rej.write("""\"{}", "{}"\n""".format(artist, title))
            return None
        first = result["tracks"]["items"][0]
    except Exception as ex:
        import pdb; pdb.set_trace()
        print (ex)
    try:
        spot_alb = first["album"]["name"]
        spot_art = first["artists"][0]["name"]
        spot_trk = first["name"]
        logging.info("    found {} :: {} => {}".format(
            spot_art,
            spot_alb,
            spot_trk,
        ))
        if (clean(title) in clean(spot_trk) and
            clean(spot_art) in clean(artist)):
            logging.info("###")
            return first["uri"]
        else:
            rej.write("""\"{}", "{}"\t\t"{} {} {}"\n""".format(
                artist, title,spot_art, spot_alb, spot_trk))
            logging.info("---")
    except Exception as ex:
        import pdb; pdb.set_trace()
        print (ex)


def main(args):
    token = spotipy.util.prompt_for_user_token(
        redirect_uri=args.redir,
        username=args.user,
        scope=scope)

    spotify = spotipy.Spotify(auth=token)
    rej = open("not_found.csv", "w")

    (tracks, tot) = get_tracks(args, spotify, rej)

    logging.info("Found {} tracks of {}".format(len(tracks), tot))
    result = spotify.user_playlist_create(args.user, args.playlist)
    batches = [tracks[i:i+100] for i in range(0, len(tracks), 100)]
    for batch in batches:
        spotify.user_playlist_add_tracks(
            args.user,
            result["uri"],
            batch,
            )
    print("Created playlist {}".format(args.playlist))

if __name__ == "__main__":
    main(args())
