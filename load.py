# Пример запуска из CLI:
# 'python load.py -json_dir C:\sqllite\three_minutes_tweets.json -db_dir C:\sqllite\tweets.db'

# Аргументы командной строки при запуске скрипта:
# json_dir - путь к файлу json (если не задан, файл берется из текущей директории)
# db_dir - путь к файлу БД (если не задан, файл берется из текущей директории)

import sqlite3
import json
import argparse
import pathlib


class DBLoad:

    def __init__(self, json_dir, db_dir):
        self.data = []
        self.json_dir = json_dir
        self.db_dir = db_dir
        self.tweet_structure = ['name', 'tweet_text', 'country_code', 'display_url', 'lang', 'created_at', 'location', 'tweet_sentiment']

    def json_read(self):
        with open(self.json_dir) as f:
            for line in f:
                self.data.append(json.loads(line))

    def json_to_db(self):
        con = sqlite3.connect(self.db_dir)
        cur = con.cursor()

        # Создание строки из json-файла для загрузки в БД
        for line in self.data:
            if 'delete' in line.keys():
                continue

            line_to_db = [None] * len(self.tweet_structure)

            if line['user']:
                if line['user']['name']:
                    line_to_db[0] = line['user']['name']

            if line['text']:
                line_to_db[1] = line['text']

            if line['place']:
                if line['place']['country_code']:
                    line_to_db[2] = line['place']['country_code']

            if line['entities']:
                if line['entities']['urls']:
                    if line['entities']['urls'][0]:
                        if line['entities']['urls'][0]['display_url']:
                            line_to_db[3] = line['entities']['urls'][0]['display_url']

            if line['lang']:
                line_to_db[4] = line['lang']

            if line['created_at']:
                line_to_db[5] = line['created_at']

            if line['user']:
                if line['user']['location']:
                    line_to_db[6] = line['user']['location']

            line_to_db[7] = 0

            # загрузка очередной строки данных в БД
            cur.execute('INSERT INTO tweets_db '
                        '(name, tweet_text, country_code, display_url, lang, created_at, location, tweet_sentiment)'
                        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        line_to_db)

        con.commit()
        con.close()


# Возможность задать путь к json-файлу и файлу БД через аргументы командной строки
parser = argparse.ArgumentParser()
parser.add_argument(
    '-json_dir',
    type=str,
    default=pathlib.Path().cwd() / 'three_minutes_tweets.json',
    help='directory for json, default - current directory'
)

parser.add_argument(
    '-db_dir',
    type=str,
    default=pathlib.Path().cwd() / 'tweets.db',
    help='directory for DB-file, default - current directory'
)
args = parser.parse_args()

# Загрузка данных в БД
dbl = DBLoad(args.json_dir, args.db_dir)
dbl.json_read()
dbl.json_to_db()
