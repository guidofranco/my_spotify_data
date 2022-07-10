from datetime import datetime, date, timedelta

def to_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%dT%X.%fZ")

def get_artist_names(artists_list):
    names = [artist["name"] for artist in artists_list]
    return ", ".join(names)

def get_song_features(songs, sp):
    songs_extended = map(
        lambda track: dict(track, **sp.audio_features(track["id"])[0]),
        songs
    )   

    return songs_extended