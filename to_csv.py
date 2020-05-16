import json
import os

import argparse

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="GMusic JSON file")
    args = parser.parse_args()
    return args

def esc(word):
    if not word:
        word = ""
    word.replace('"', '\\"')
    word.replace('|','\\|')
    return word

def main(args):
    ff = open(args.data)
    data = json.load(ff)
    print("Artist|Title|Album|Cover Art")
    for record in data[1][0]:
        (guid, title, cover, artist, album, *data) = record
        print ('"{artist}"|"{title}"|"{album}"|"{cover}"'.format(
        artist=esc(artist),
        title=esc(title),
        album=esc(album),
        cover=esc(cover),
        ))

if __name__ == "__main__":
    main(args())