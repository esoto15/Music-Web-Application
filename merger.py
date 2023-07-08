import pandas
# -- this class merges two csv files based on a similar column--


def main():
    # merge1('albums.csv', 'artists.csv')
    merge2('Tracks.csv', 'albums.csv')


# -- albums file merged with artist, to get genre id--
def merge1(file1, file2):
    csv1 = pandas.read_csv(file1)
    csv2 = pandas.read_csv(file2)
    merged = csv1.merge(csv2, on='artist_id')
    merged.to_csv("albums.csv", index=False)


# --track file--
def merge2(file1, file2):
    csv1 = pandas.read_csv(file1)
    csv2 = pandas.read_csv(file2)
    merged = csv1.merge(csv2, on='album_id')
    merged.to_csv("tracklist.csv", index=False)


if __name__ == '__main__':
    main()