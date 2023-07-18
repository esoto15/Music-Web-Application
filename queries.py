# --MySQL Connection--
import pymysql


def sql_connector():
    conn = pymysql.connect(user='root', password='7845',
                           db='music', host='localhost', port=3306)
    c = conn.cursor()
    return conn, c


def create_genres_table_query():
    conn, c = sql_connector()
    query = """
    CREATE TABLE IF NOT EXISTS genres (
        genre_id INT AUTO_INCREMENT PRIMARY KEY,
        genre_name VARCHAR(255)
    );
    """
    c.execute(query)
    conn.commit()
    c.close()


def create_artists_table_query():
    conn, c = sql_connector()
    query = """
    CREATE TABLE IF NOT EXISTS artists (
        artist_id INT PRIMARY KEY AUTO_INCREMENT,
        genre_id INT,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        nationality VARCHAR(255),
        age INT,
        FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
    )
    """
    c.execute(query)
    conn.commit()
    c.close()


def create_albums_table_query():
    conn, c = sql_connector()
    query = """
    CREATE TABLE IF NOT EXISTS album (
        album_id INT AUTO_INCREMENT PRIMARY KEY,
        artist_id INT,
        genre_id INT,
        album_name VARCHAR(255),
        FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
        FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
    )
    """
    c.execute(query)
    conn.commit()
    c.close()


def create_users_table_query():
    conn, c = sql_connector()
    query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255),
            PRIMARY KEY (user_id)
        )
    """
    c.execute(query)
    conn.commit()
    conn.close()


def create_tracks_table():
    conn, c = sql_connector()
    query = """
    CREATE TABLE IF NOT EXISTS tracks (
      track_id INT AUTO_INCREMENT,
      album_id INT,
      artist_id INT,
      genre_id INT,
      song_title VARCHAR(255),
      song_length INT,
      PRIMARY KEY (track_id),
      FOREIGN KEY (album_id) REFERENCES album(album_id),
      FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
      FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
    );
    """
    c.execute(query)
    conn.commit()
    conn.close()
