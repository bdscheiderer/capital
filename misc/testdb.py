# this simply creats a test-starting database

import sqlite3, datetime

# create test data
test_data = [
(20, 0),(20, 0),(20, 2),(20, 2),(20, 3),
(20, 20),(20, 20),(20, 20),(20, 20),(20, 20),
(20, 13),(20, 14),(20, 15),(20, 16),(20, 17),
(20, 15),(20, 15),(20, 16),(20, 16),(20, 17),
(20, 18),(20, 18),(20, 15),(20, 16),(20, 17),
(50, 0),(50, 0),(50, 2),(50, 3),(50, 15),
(50, 50),(50, 50),(50, 50),(50, 50),(50, 50),
(50, 20),(50, 30),(50, 35),(50, 40),(50, 41),
(50, 40),(50, 43),(50, 45),(50, 45),(50, 47),
(50, 43),(50, 45),(50, 45),(50, 47),(50, 49)]

date = '17-12-25'

# create database if it does not exist
conn = sqlite3.connect('capital_db.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Scores
    (id INTEGER PRIMARY KEY UNIQUE,
     datestamp TEXT,
     quiz INTEGER,
     score INTEGER)''')

# add test data to database
for item in test_data:
    print(date, item[0], item[1])
    cur.execute('INSERT INTO Scores (datestamp, quiz, score) VALUES (?, ?, ?)', (date, item[0], item[1],))

conn.commit()

print('Done inserting, now printing...')

cur.execute('SELECT score FROM Scores WHERE quiz=20 AND score=20')
dat = cur.fetchall()

print(dat)
for row in dat:
    print(row)

print('Done')

# close database
cur.close()
conn.close()
