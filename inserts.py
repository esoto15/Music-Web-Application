import csv

import pymysql
from csv import DictReader


# --MySQL Connection--
def sql_connector():
    conn = pymysql.connect(user='root', password='7845', db='Music_Application', host='localhost')
    c = conn.cursor()
    return conn, c


# --file opener--
def opener(file):
    with open(file, 'r+', encoding='utf8') as f:
        dict_reader = DictReader(f)
        list_of_dict = list(dict_reader)
        return list_of_dict


# --main--
def main():
    # --insert primary tables--
    #  insert_genres("genres.csv")
    # insert_users("users.csv")
    # insert_artists("artists.csv")
    # insert_albums("albums.csv")
    # insert_tracks("tracks.csv")
    insert_comments("comments.csv")
    # display_genres()
    # display_artists("genres")
    # display_users()


# -----methods for inserting files-----
def insert_genres(file):
    conn, c = sql_connector()
    list_of_dict = opener(file)
    for row in list_of_dict:
        genre_name = row["genre_name"]
        query = "INSERT INTO genres (name) VALUES('{}')".format(genre_name)
        c.execute(query)
        conn.commit()
    conn.close()
    c.close()


def display_genres():
    conn, c = sql_connector()
    query = "select (name) from genres order by name DESC"
    c.execute(query)
    result = c.fetchall()
    print(result)
    for x in result:
        print(x[0])


def insert_users(file):
    conn, c = sql_connector()
    list_of_dict = opener(file)
    for row in list_of_dict:
        first_name = row["first_name"]
        last_name = row["last_name"]
        email = row["email"]
        password = row["password"]
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES ('{}','{}', '{}', '{}')".format(first_name, last_name, email, password)
        c.execute(query)
        conn.commit()
    conn.close()
    c.close()


def display_users():
    conn, c = sql_connector()
    email = "esoto15@neiu.ed8"
    query = 'select COUNT(user_ID) from users where email=' + "'{}'".format(email)
    c.execute(query)
    if len(c.fetchall()) == 0:
        print("zero")
    elif len(c.fetchall()):
        count = [row[0] for row in c.fetchall() if row[0]]
        print(count[0])
        conn.close()
        c.close()


def insert_artists(file):    # artists jointed with albums
    conn, c = sql_connector()
    list_of_dict = opener(file)
    for row in list_of_dict:
        genre_id = row["genre_id"]
        first_name = row["first_name"]
        last_name = row["last_name"]
        nationality = row["nationality"]
        age = row["age"]
        query = 'INSERT INTO artists (genre_id, first_name, last_name, nationality, age) VALUES ({},"{}", "{}", "{}", {})'.format(int(genre_id), first_name, last_name, nationality, int(age))
        c.execute(query)
        conn.commit()
    conn.close()
    c.close()


def display_artists(chosen):
    conn, c = sql_connector()
    query = "SELECT A.first_name AS First_Name, A.last_name AS Last_name, GENRES.name AS Genre FROM ARTISTS AS A INNER JOIN GENRES ON A.genre_ID = GENRES.genreID ORDER BY A.first_name ASC;"
    c.execute(query)
    result = c.fetchall()
    print(result)
    for x in result:
        print(x[0], " ", x[1], " ", x[2])


def insert_albums(file):
    conn, c = sql_connector()
    list_of_dict = opener(file)
    for row in list_of_dict:
        genre_id = row["genre_id"]
        album_id = row["album_id"]
        artist_id = row["artist_id"]
        album_name = row["album_name"]
        query = 'INSERT INTO album (album_id, artist_id, genre_id, album_name) VALUES ({}, {}, {}, "{}")'.format(int(album_id), int(artist_id), int(genre_id), album_name)
        c.execute(query)
        conn.commit()
    conn.close()
    c.close()


def insert_tracks(file):
    conn, c = sql_connector()
    list_of_dict = opener(file)
    for row in list_of_dict:
        genre_id = row["genre_id"]
        album_id = row["album_id"]
        artist_id = row["artist_id"]
        title = row["song_title"]
        track_id = row["track_id"]
        song_length = row["song_length"]
        query = 'INSERT INTO tracklist (trackid,album_id,artist_id,genre_id, title,songLength) VALUES ({}, {}, {},{}, "{}","{}")'.format(int(track_id), int(album_id), int(artist_id), int(genre_id), title, song_length)
        c.execute(query)
        conn.commit()
    conn.close()
    c.close()


# Insert comments!
def insert_comments(file):
    conn, cursor = sql_connector()
    list_of_dict = opener(file)
    for row in list_of_dict:
        user_id = int(row["user_id"])
        artist_id = int(row["artist_id"])
        comment_text = row["comment_text"]
        likes = int(row["likes"])
        query = 'INSERT INTO COMMENTS (user_ID, artist_ID, comment_text, likes) VALUES ({}, {}, "{}", {})'.format(user_id, artist_id, comment_text, likes)
        cursor.execute(query)
        conn.commit()
    conn.close()
    cursor.close()


if __name__ == '__main__':
    main()