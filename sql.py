import pymysql.cursors
import unittests
from datetime import date

class SpotSQL:
    # move values to another file...
    def __init__():
        self.connection = pymysql.connect(host='10.43.112.2',
                                            user='root',
                                            password='test',
                                            db=None,
                                            charset='utf8',
                                            cursorclass=pymysql.cursors.DictCursor)

    def add_user(username):
        self.connection.select_db('users')
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
        self.connection.select_db('users')
        with self.users_conn.cursor() as cursor:
            sql = """INSERT INTO %s ('date', 'q1', 'q2', 'q3', 'q4', 'song', 'emotion', 'token')
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (username, date, q1, q2, q3, q4, song, emotion, token,))
        
        self.users_conn.commit()

    def get_user_entry(date, username):
        self.connection.select_db('users')
        with self.users_conn.cursor() as cursor:
            sql = "SELECT * FROM %s WHERE 'date'=%s"
            cursor.execute(sql, (username, date,))
            return cursor.fetchall()

    def add_song(song):
        self.connection.select_db('songs')
        with self.songs_conn.cursor() as cursor:
            sql = """IF EXISTS( SELECT * FROM INFORMATION_SCHEMA.TABLES
                        WHERE TABLE_NAME = %s)
                        SELECT NULL
                        ELSE CREATE TABLE %s(emotion TEXT);"""
            cursor.execute(sql, (song,))
        
        self.songs_conn.commit()

    def add_emotion(song, emotion):
        self.connection.select_db('songs')
        with self.songs_conn.cursor() as cursor:
            sql = "INSERT INTO %s ('emotion') VALUES (%s)"
            cursor.execute(sql, (song, emotion,))
        
        self.songs_conn.commit()
    
    def get_songs_emotes(song):
        self.connection.select_db('songs')
        with self.songs_conn.cursor() as cursor:
            sql = "SELECT 'emotion' FROM %s"
            cursor.execute(sql, (song,))
            return cursor.fetchall()

    def get_user_songs(username):
        self.connection.select_db('users')
        with self.users_conn.cursor() as cursor:
            sql = "SELECT 'songs' FROM %s"
            cursor.execute(sql, (username,))
            return cursor.fetchall()

class TestSQLMethods(unittests.TestCase):

    self.db = SpotSQL()

    self.u_data1 = {'username' : 'user1', 'date' : date.today(), 'q1': 'answer', 'q2' : 'answer', 'q3' : 'answer', 'q4' : 'answer', 'song' : 'fun song', 'emotion' : 'happy', 'token' : 'asdfg'}
    self.u_data2 = {'username' : 'user2', 'date' : date.today(), 'q1': 'answer', 'q2' : 'answer', 'q3' : 'answer', 'q4' : 'answer', 'song' : 'bad song', 'emotion' : 'sad', 'token' : 'asdfg'}
    self.u_data3 = {'username' : 'user3', 'date' : date.today(), 'q1': 'answer', 'q2' : 'answer', 'q3' : 'answer', 'q4' : 'answer', 'song' : 'jump song', 'emotion' : 'excited', 'token' : 'asdfg'}

    self.s_data1 = ['good song', 'happy', 'happy', 'excited', 'indifferent', 'excited', 'happy']
    self.s_data2 = ['better song', 'sad', 'sad', 'sad', 'relaxed', 'relaxed', 'angry', 'sad']
    self.s_data3 = ['best song', 'angry', 'angry', 'sad', 'happy', 'happy', 'angry', 'sad']

    def test_add1(self):
        self.db.add_user(self.u_data1.values[0])
        self.db.add_user_entry(self.u_data1.values[0], self.u_data1.values[1], self.u_data1.values[2], self.u_data1.values[3], self.u_data1.values[4], self.u_data1.values[5], self.u_data1.values[6], self.u_data1.values[7], self.u_data1.values[8])
        self.db.add_song(self.s_data1[0])
        self.db.add_emotion(self.s_data1[1])
        
        tdata = self.u_data1.pop('username')
        self.assertEqual(self.db.get_user_entry(self.u_data1.values[0], self.u_data1.values[1]), tdata)
        self.assertEqual(self.db.get_songs_emotes(self.s_data1[0]), ['happy'])