import MySQLdb


try:
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         passwd='root')
    cur = db.cursor()
    cur.execute("CREATE DATABASE %s;" % 'nba')
    db.close()
    print("Database created!")
except:
    print("Something went wrong during creating database!")
