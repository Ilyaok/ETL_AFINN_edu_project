import sqlite3
import json

data = []
with open('three_minutes_tweets.json') as f:
    for line in f:
        data.append(json.loads(line))

con = sqlite3.connect('tweets.db')
cur = con.cursor()

# todo оптимизировать ситуацию с else (в т.ч. проверить вложенные if)
for line in data:
    if 'delete' not in line.keys():
        line_to_db = []

        if line['user']:
            if line['user']['name']:
                line_to_db.append(line['user']['name'])
            else:
                line_to_db.append(None)
        else:
            line_to_db.append(None)

        if line['text']:
            line_to_db.append(line['text'])
        else:
            line_to_db.append(None)

        if line['place']:
            if line['place']['country_code']:
                line_to_db.append(line['place']['country_code'])
            else:
                line_to_db.append(None)
        else:
            line_to_db.append(None)

        if line['entities']:
            if line['entities']['urls']:
                if line['entities']['urls'][0]:
                    if line['entities']['urls'][0]['display_url']:
                        line_to_db.append(line['entities']['urls'][0]['display_url'])
                    else:
                        line_to_db.append(None)
                else:
                    line_to_db.append(None)
            else:
                line_to_db.append(None)
        else:
            line_to_db.append(None)

        if line['lang']:
            line_to_db.append(line['lang'])
        else:
            line_to_db.append(None)

        if line['created_at']:
            line_to_db.append(line['created_at'])
        else:
            line_to_db.append(None)

        if line['user']:
            if line['user']['location']:
                line_to_db.append(line['user']['location'])
            else:
                line_to_db.append(None)
        else:
            line_to_db.append(None)

        line_to_db.append(0)

        # загрузка в БД
        cur.execute('INSERT INTO tweets_db '
                    '(name, tweet_text, country_code, display_url, lang, created_at, location, tweet_sentiment)'
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    line_to_db)

con.commit()
con.close()
