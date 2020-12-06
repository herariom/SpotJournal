import pymysql.cursors


class SpotSQL:
    # move values to another file...
    def __init__():
        self.users_conn = pymysql.connect(host='10.43.112.2',
                                            user='root',
                                            password='test',
                                            db='users',
                                            charset='utf8',
                                            cursorclass=pymysql.cursors.DictCursor)
        
        self.songs_conn = pymysql.connect(host='10.43.112.2',
                                            user='root',
                                            password='test',
                                            db='songs',
                                            charset='utf8',
                                            cursorclass=pymysql.cursors.DictCursor)

    def add_user(username):
        with self.users_conn.cursor() as cursor:
            sql = """IF EXISTS( SELECT * FROM INFORMATION_SCHEMA.TABLES
                        WHERE TABLE_NAME = %s)
                        SELECT NULL
                        ELSE CREATE TABLE %s (date DATE, q1 TEXT, q2 TEXT, 
                                                q3 TEXT, q4 TEXT, song TEXT,
                                                emotion TEXT, token TEXT);"""
            cursor.execute(sql, (username,))
        
        self.users_conn.commit()
    
    def add_user_entry(username, date, q1, q2, q3, q4, song, emotion, token):
        with self.users_conn.cursor() as cursor:
            sql = """INSERT INTO %s ('date', 'q1', 'q2', 'q3', 'q4', 'song', 'emotion', 'token')
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s %s)"""
            cursor.execute(sql, (username, date, q1, q2, q3, q4, song, emotion, token,))
        
        self.users_conn.commit()

    def get_user_entry(date, username):
        with self.users_conn.cursor() as cursor:
            sql = "SELECT * FROM %s WHERE 'date'=%s"
            cursor.execute(sql, (username, date,))
            return cursor.fetchone()

    def add_song(song):
        with self.songs_conn.cursor() as cursor:
            sql = """IF EXISTS( SELECT * FROM INFORMATION_SCHEMA.TABLES
                        WHERE TABLE_NAME = %s)
                        SELECT NULL
                        ELSE CREATE TABLE %s(emotion TEXT);"""
            cursor.execute(sql, (song,))
        
        self.songs_conn.commit()

    def add_emotion(song, emotion):
        with self.songs_conn.cursor() as cursor:
            sql = "INSERT INTO %s ('emotion') VALUES (%s)"
            cursor.execute(sql, (song, emotion,))
        
        self.songs_conn.commit()
    
    def get_songs_emotes(song):
         with self.songs_conn.cursor() as cursor:
            sql = "SELECT 'emotion' FROM %s"
            cursor.execute(sql, (song,))
            return cursor.fetchone()

    def get_user_songs(username):
        with self.users_conn.cursor() as cursor:
            sql = "SELECT 'songs' FROM %s"
            cursor.execute(sql, (username,))
            return cursor.fetchone()