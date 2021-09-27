import sqlite3
import json

data = []
with open('three_minutes_tweets.json') as f:
    for line in f:
        data.append(json.loads(line))


con = sqlite3.connect('tweets.db')
cur = con.cursor()

def check_exists(l, val):
    pass



# В условии задачи не уточнено, что делать с твитами в статусе 'delete'
# Принято решение не загружать такие твиты в БД
for line in data:
    if 'delete' not in line.keys():
        line_to_db = []
        line_to_db.append(line['id'])
        check_exists(line_to_db, line['user']['name'])
        check_exists(line_to_db, line['text'])
        check_exists(line_to_db, line['place']['country_code'])
        check_exists(line_to_db, line['entities']['urls'][0]['display_url'])
        check_exists(line_to_db, line['lang'])
        check_exists(line_to_db, line['created_at'])
        check_exists(line_to_db, line['user']['location'])
        print(line_to_db)

#todo проверить кодировку
cur.execute('INSERT INTO tweets_test '
            '(id, name, tweet_text, country_code, display_url, lang, created_at, location, tweet_sentiment)'
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (data[4]['id'],
             data[4]['user']['name'],
             data[4]['text'],
             data[117]['place']['country_code'],
             data[21]['entities']['urls'][0]['display_url'], #data[4]['entities']['media'][0]['indices']['display_url'],
             data[4]['lang'],
             data[4]['created_at'],
             data[4]['user']['location'],
             0))


a, b = 111, 222
d = {1: 'a'}
l = [123, 456]
cur.execute('INSERT INTO test VALUES (?, ?)', l)

con.commit()

con.close()