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

    def json_to_db(self):
        with open(self.json_dir) as f:
            for line in f:
                self.data.append(json.loads(line))

        con = sqlite3.connect(self.db_dir)
        cur = con.cursor()

        # Создание строки из json-файла для загрузки в БД
        for line in self.data:
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

# Создание экземляра класса Загрузки и загрузка данных в БД
dbl = DBLoad(args.json_dir, args.db_dir)
dbl.json_to_db()
