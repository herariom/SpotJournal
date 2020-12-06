import pymysql.cursors
import unittest
from datetime import date

class SpotSQL:
    # move values to another file...
    def __init__(self):
        self.connection = pymysql.connect(host='34.66.19.176',
                                          user='root',
                                          password='test',
                                          db=None,
                                          charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor)

    def add_user(self, username):
        self.connection.select_db('users')
        with self.connection.cursor() as cursor:
            sql = "SHOW TABLES"
            cursor.execute(sql)
            result = cursor.fetchall()

            for x in result:
                if x.get('Tables_in_users') == "'" + username + "'":
                    return

            sql = "CREATE TABLE `%s` (date DATE NULL, q1 TEXT NULL, q2 TEXT NULL, q3 TEXT NULL, q4 TEXT NULL, song TEXT NULL, emotion TEXT NULL, token TEXT NULL);"

            cursor.execute(sql, (username,))
        self.connection.commit()

    def add_user_entry(self, username, tdate, q1, q2, q3, q4, song, emotion, token):
        self.connection.select_db('users')
        with self.connection.cursor() as cursor:
            sql = """INSERT INTO `%s` (`date`, `q1`, `q2`, `q3`, `q4`, `song`, `emotion`, `token`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (username, tdate, q1, q2, q3, q4, song, emotion, token,))

        self.connection.commit()

    def get_user_entry(self, tdate, username):
        self.connection.select_db('users')
        with self.connection.cursor() as cursor:

            sql = "SELECT * FROM `%s` WHERE date=%s"
            cursor.execute(sql, (username, tdate,))

            return cursor.fetchone()

    def add_song(self, song):
        self.connection.select_db('songs')
        with self.connection.cursor() as cursor:
            sql = "SHOW TABLES"
            cursor.execute(sql)
            result = cursor.fetchall()

            for x in result:
                if x.get('Tables_in_songs') == "'" + song + "'":
                    return

            sql = "CREATE TABLE `%s` (emotion TEXT)"
            cursor.execute(sql, (song,))

        self.connection.commit()

    def add_emotion(self, song, emotion):
        self.connection.select_db('songs')
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `%s` (`emotion`) VALUES (%s)"
            cursor.execute(sql, (song, emotion,))

        self.connection.commit()

    def get_songs_emotes(self, song):
        self.connection.select_db('songs')
        with self.connection.cursor() as cursor:
            sql = "SELECT emotion FROM `%s`"
            cursor.execute(sql, (song,))
            return self.result_to_list(cursor.fetchall())

    def get_user_songs(self, username):

        self.connection.select_db('users')
        with self.connection.cursor() as cursor:
            print('sql.py ' + username)
            sql = "SELECT song FROM `%s`"
            cursor.execute(sql, (username,))
            return self.result_to_list(cursor.fetchall())

    def result_to_list(self, result):
        list = []
        for x in result:
            for (k, v) in x.items():
                list.append(v)
        
        return list

class TestSQLMethods(unittest.TestCase):

    def __init__(self):
        self.db = SpotSQL()

        self.u_data1 = {'username': 'user1', 'date': date.today(), 'q1': 'answer', 'q2': 'answer', 'q3': 'answer',
                   'q4': 'answer', 'song': 'fun song', 'emotion': 'happy', 'token': 'asdfg'}
        self.u_data2 = {'username': 'user2', 'date': date.today(), 'q1': 'answer', 'q2': 'answer', 'q3': 'answer',
                   'q4': 'answer', 'song': 'bad song', 'emotion': 'sad', 'token': 'asdfg'}
        self.u_data3 = {'username': 'user3', 'date': date.today(), 'q1': 'answer', 'q2': 'answer', 'q3': 'answer',
                   'q4': 'answer', 'song': 'jump song', 'emotion': 'excited', 'token': 'asdfg'}

        self.s_data1 = ['good song', 'happy', 'happy', 'excited', 'indifferent', 'excited', 'happy']
        self.s_data2 = ['better song', 'sad', 'sad', 'sad', 'relaxed', 'relaxed', 'angry', 'sad']
        self.s_data3 = ['best song', 'angry', 'angry', 'sad', 'happy', 'happy', 'angry', 'sad']

    def test_add1(self):
        self.db.add_user(self.u_data1.get('username'))
        self.db.add_user_entry(self.u_data1.get('username'), self.u_data1.get('date'), self.u_data1.get('q1'),
                               self.u_data1.get('q2'), self.u_data1.get('q3'), self.u_data1.get('q4'),
                               self.u_data1.get('song'), self.u_data1.get('emotion'), self.u_data1.get('token'))
        self.db.add_song(self.s_data1[0])
        self.db.add_emotion(self.s_data1[0], self.s_data1[1])

        #self.assertEqual(self.db.get_user_entry(date.today(), self.u_data1.get('username')), [{'date': date.today(), 'q1': 'answer', 'q2': 'answer', 'q3': 'answer', 'q4': 'answer', 'song': 'fun song', 'emotion': 'happy', 'token': 'asdfg'}])
        #self.assertEqual(self.db.get_songs_emotes(self.s_data1[0]), ['happy'])

#test = TestSQLMethods()
#test.test_add1()