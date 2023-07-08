from flask import Flask, request, render_template, url_for, flash, redirect, session
import pymysql
from itertools import zip_longest

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# --MySQL Connection--
def sql_connector():
    conn = pymysql.connect(user='root', password='7845',
                           db='Music_Application', host='localhost')
    c = conn.cursor()
    return conn, c


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/genres')
def genres():
    conn, c = sql_connector()
    genres = ['rock', 'pop', 'Electronic', 'R&B', "country", "Indie"]
    colors = [' #91A3B0', ' #91A3B0', ' #91A3B0', ' #91A3B0', " #91A3B0", " #91A3B0"]
    genres_and_colors = zip_longest(genres, colors, fillvalue='')
    # Query-1
    c.execute("SELECT COUNT(genres.genreid) FROM GENRES")
    count = c.fetchone()[0]
    return render_template('genres.html', genres_and_colors=genres_and_colors, count=count)


@app.route('/artists', methods=['GET'])
def artists():
    conn, c = sql_connector()
    artists_data = []
    # ---Inputs----
    sort = request.args.get('sort', 'first_name_asc')
    search_text = request.args.get('search_text', '')
    submit_nationality = request.args.get('submit_nationality')
    submit_age = request.args.get('submit_age')

    if submit_nationality:
        # -----Query-2--------
        sql = "SELECT A.artist_ID, A.first_name, A.last_Name, COUNT(B.album_ID) AS AlbumsReleased, GENREs.name AS Genre, A.nationality " \
              "FROM ARTISTS AS A " \
              "INNER JOIN GENRES ON A.genre_ID = GENREs.genreID " \
              "INNER JOIN ALBUM AS B ON A.artist_ID=B.artist_ID " \
              "WHERE A.nationality = %s " \
              "GROUP BY A.artist_ID " \
              "ORDER BY A.First_Name ASC"
        c.execute(sql, (search_text,))
        artists_data = c.fetchall()
        # ------Query-3-----
        sql2 = "SELECT COUNT(*) AS TotalArtists, AVG(AlbumsReleased) AS AvgAlbumsReleased FROM (SELECT A.artist_ID, COUNT(B.album_ID) AS AlbumsReleased FROM ARTISTS AS A INNER JOIN ALBUM AS B ON A.artist_ID=B.artist_ID WHERE A.nationality = %s GROUP BY A.artist_ID) AS AlbumsByArtist"
        c.execute(sql2, (search_text,))
        second_data = c.fetchall()
        return render_template('artists.html', artists_data=artists_data, second_data=second_data)
    elif submit_age:
        # ------ Query 4! ----
        sql = "SELECT A.artist_ID, A.first_name, A.last_Name, COUNT(B.album_ID) AS AlbumsReleased, GENREs.name AS Genre " \
              "FROM ARTISTS AS A " \
              "INNER JOIN GENRES ON A.genre_ID = GENREs.genreID " \
              "INNER JOIN ALBUM AS B ON A.artist_ID=B.artist_ID " \
              "WHERE A.age = %s " \
              "GROUP BY A.artist_ID " \
              "ORDER BY A.First_Name ASC"
        c.execute(sql, (search_text,))
        artists_data = c.fetchall() 
        # -----Query-5--------
        sql3 = "SELECT COUNT(*) AS total_artists, round(AVG(album_count),1) AS avg_albums " \
              "FROM ( " \
              "SELECT COUNT(album_ID) AS album_count " \
              "FROM ARTISTS " \
              "JOIN ALBUM ON ARTISTS.artist_ID = ALBUM.artist_ID " \
              "WHERE age = %s " \
              "GROUP BY ARTISTS.artist_ID " \
              ") AS albums_released"
        c.execute(sql3, (search_text,))
        second_data = c.fetchall()
        return render_template('artists.html', artists_data=artists_data, second_data=second_data)
    #     --Query 7-
    if sort == 'first_name_asc':
        sql = "SELECT A.artist_ID, A.first_name, A.last_Name, COUNT(B.album_ID) AS AlbumsReleased, GENREs.name AS Genre " \
              "FROM ARTISTS AS A " \
              "INNER JOIN GENRES ON A.genre_ID = GENREs.genreID " \
              "INNER JOIN ALBUM AS B ON A.artist_ID=B.artist_ID " \
              "GROUP BY A.artist_ID " \
              "ORDER BY A.First_Name ASC"
    elif sort == 'first_name_desc':
        sql = "SELECT A.artist_ID, A.first_name, A.last_Name, COUNT(B.album_ID) AS AlbumsReleased, GENREs.name AS Genre " \
              "FROM ARTISTS AS A " \
              "INNER JOIN GENRES ON A.genre_ID = GENREs.genreID " \
              "INNER JOIN ALBUM AS B ON A.artist_ID=B.artist_ID " \
              "GROUP BY A.artist_ID " \
              "ORDER BY A.First_Name DESC"
    elif sort == 'albums_asc':
        sql = "SELECT A.artist_ID, A.First_Name AS First_Name, A.Last_Name AS Last_name, COUNT(B.album_ID) AS AlbumsReleased, GENREs.name AS Genre " \
              "FROM ARTISTS AS A " \
              "INNER JOIN GENRES ON A.genre_ID = GENREs.genreID " \
              "INNER JOIN ALBUM AS B ON A.artist_ID=B.artist_ID " \
              "GROUP BY A.artist_ID " \
              "ORDER BY AlbumsReleased ASC, A.First_Name ASC"
    elif sort == 'albums_desc':
        sql = "SELECT A.artist_ID, A.First_Name AS First_Name, A.Last_Name AS Last_name, COUNT(B.album_ID) AS AlbumsReleased, GENREs.name AS Genre " \
              "FROM ARTISTS AS A " \
              "INNER JOIN GENRES ON A.genre_ID = GENREs.genreID " \
              "INNER JOIN ALBUM AS B ON A.artist_ID=B.artist_ID " \
              "GROUP BY A.artist_ID " \
              "ORDER BY AlbumsReleased DESC, A.First_Name ASC"
    c.execute(sql)
    artists_data = c.fetchall()
    return render_template('artists.html', artists_data=artists_data)


@app.route('/profiles')
def profiles():
    artist_id = request.args.get('artist_id', default=None, type=int)
    if artist_id is None:
        return redirect(url_for('artists'))
    conn, c = sql_connector()
    # ---Query 5---
    sql_query = """
        SELECT A.first_name, A.last_name, A.nationality, A.age, B.album_name, Tracklist.title AS song, Tracklist.songLength
        FROM ARTISTS AS A 
        INNER JOIN ALBUM AS B ON A.artist_ID = B.artist_ID 
        INNER JOIN TRACKLIST ON B.album_ID = TRACKLIST.album_ID
        WHERE A.artist_ID = %s
        GROUP BY A.artist_ID, B.album_name,Tracklist.title, Tracklist.songlength;
    """
    c.execute(sql_query, (artist_id,))
    artist_data = c.fetchall()
    if not artist_data:
        return redirect(url_for('artists'))

        # Query to get comments and likes for an artist
    sql_query = """
            SELECT U.first_name, U.last_name, C.comment_text, C.likes
            FROM USERS AS U
            INNER JOIN COMMENTS AS C ON U.user_ID = C.user_ID
            INNER JOIN ARTISTS AS A ON C.artist_ID = A.artist_ID
            WHERE A.artist_ID = %s;
        """
    c.execute(sql_query, (artist_id,))
    comments = c.fetchall()

    first_name, last_name, nationality, age = artist_data[0][:4]
    album_names = [album[4] for album in artist_data]
    songs = [album[5] for album in artist_data]
    songlength = [album[6] for album in artist_data]

    return render_template('profiles.html', artist_id=str(artist_id), first_name=first_name, last_name=last_name,
                               nationality=nationality, age=age, album_names=album_names, songs=songs,
                               songlength=songlength, comments=comments)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn, c = sql_connector()
        username = request.form['email']
        password = request.form['password']
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        c.execute(query, (username, password))
        result = c.fetchone()
        if result is not None:
            # Check if the logged-in user is an admin
            admin_query = "SELECT * FROM ADMINISTRATORS WHERE email = %s"
            c.execute(admin_query, (username,))
            admin_result = c.fetchone()
            conn.close()
            if admin_result is not None:
                session['logged_in'] = True
                return redirect(url_for('dashboard'))
            else:
                session['logged_in'] = True
                return redirect(url_for('home'))
        else:
            return 'Incorrect username or password'
    else:
        return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    msg= "User not Found! :("
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        conn, c = sql_connector()
        # -----Query 9---
        query = "SELECT * FROM USERS WHERE first_name = %s AND last_name = %s"
        c.execute(query, (first_name, last_name))
        results = c.fetchall()
        conn.close()
        return render_template("dashboard.html", users=results)
    else:
        return render_template("dashboard.html", msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    conn, c = sql_connector()
    if request.method == 'POST':
        # GET THE DATA
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        # -----Query 8--
        query = "SELECT * FROM users WHERE email = %s"
        c.execute(query, (email,))
        result = c.fetchone()

        if result is not None:
            return 'Email address already in use'

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
        c.execute(query, (first_name, last_name, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
