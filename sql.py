import pymysql.cursors

connection = pymysql.connect(host='10.43.112.2',
                             user='root',
                             password='test',
                             db='test',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

