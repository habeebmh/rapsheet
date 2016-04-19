import re
from difflib import SequenceMatcher

import nltk

import lyrics

def get_as_string(file):
    with open(file, 'r') as myfile:
        return myfile.read().replace('\n', '')


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def tokenize(line):
    line.strip()
    tokens = nltk.word_tokenize(line)
    tagged = nltk.pos_tag(tokens)
    line_tags = []
    for t in tagged:
        line_tags.append(t)
    return line_tags


def do_comparison(artist, song):
    track_id = lyrics.get_track_id_for_keywords_and_artists(song, artist)
    lyr = lyrics.get_lyrics_for_track_id(track_id)
    if lyr is None:
        return ""
    song = re.sub("\(.*\)", "", lyr)
    lines = str.split(song, "\n")
    words = ""
    tags = ""
    for line in lines:
        for t in tokenize(line):
            words += t[0] + " "
            tags += t[1] + " "

    words.replace("...  ******* This Lyrics is NOT for Commercial use *******", "").strip()
    tags.replace("...  ******* This Lyrics is NOT for Commercial use *******", "").strip()

    b_score_l = similar(get_as_string("../belligerent/all_belligerent_l.txt"), words)
    c_score_l = similar(get_as_string("../conscious/all_conscious_l.txt"), words)

    b_score_t = similar(get_as_string("../belligerent/all_belligerent_t.txt"), tags)
    c_score_t = similar(get_as_string("../conscious/all_conscious_t.txt"), tags)

    b_score = abs(b_score_l - b_score_t)
    c_score = abs(c_score_l - c_score_t)

    return ("conscious" if c_score < b_score else "belligerent") + "," + str(abs(c_score - b_score))


def similar_artist(type):
    pass


def save_data(lyrics):
    pass


def create_result(artist, song):
    comp = do_comparison(artist, song).split(",")
    # track_id = lyrics.get_track_id_for_keywords_and_artists(keywords=song, artist=artist)
    # print(track_id)
    # album = lyrics.get_album_info(track_id)
    fout = open("../result.html", 'w')
    fout.write("<html> <head> </head> <body> <h2>Results for " + song + " by " + artist +
               "</h2> <div align=\"center\"> <h1>" +
               comp[0] + "</h1> <p>With a difference of : " + str(float(comp[1]) * 100) +
               "%</p> </div> </body> </html>")
    fout.close()


create_result("Kendrick Lamar", "Alright")
