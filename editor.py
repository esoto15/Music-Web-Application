import pandas as pd


# --This file, deletes certain columns from a merged csv file--
def main():
    # albums_edit("output.csv")
    track_edit("tracklist.csv")


def albums_edit(file):
    f = pd.read_csv("output.csv")
    keep_col = ['album_id', 'artist_id', 'genre_id_y', 'album_name']
    new_f = f[keep_col]
    new_f.to_csv("albums.csv", index=False)


def track_edit(file):
    f = pd.read_csv(file)
    keep_col = ['track_id', 'album_id', 'artist_id_y', 'genre_id_y', 'song_title', 'song_length']
    new_f = f[keep_col]
    new_f.to_csv("tracks2.csv", index=False)


if __name__ == '__main__':
    main()