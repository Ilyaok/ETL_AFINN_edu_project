# Методика расчета AFINN: http://www2.imm.dtu.dk/pubdb/edoc/imm6975.pdf
# В задании не уточнено, следует ли использовать библиотеку, https://github.com/fnielsen/afinn
# Исходя из формулировки задания принято решение написать скрипт на основе AFINN самостоятельно

import sqlite3
import sys
from unicodedata import category


class SentimentCount:
    def __init__(self, afinn_path, db_path):
        self.afinn_path = afinn_path
        self.db_path = db_path
        self.valids = []
        self.score = 0
        self.st = []
        self.tweet_sentiments = {}

        # Создание словаря из файла AFINN-111.txt
        self.lexicon = {}
        with open(self.afinn_path) as f:
            for line in f:
                self.lexicon[' '.join(line.split()[:-1])] = int(line.split()[-1])

        # Создание словаря знаков препинания из таблицы Unicode
        self.codepoints = range(sys.maxunicode + 1)
        self.punctuation = {c for i in self.codepoints if category(c := chr(i)).startswith("P")}
        self.punctuation.update({' ', '\n', '\t'})
        self.punctuation.remove('@')
        self.punctuation.remove("'")

    # Подготовка строки к анализу AFINN (очистка)
    def clear_str(self, st):
        self.st = st.lower().strip()
        self.valids = []
        for i in range(len(self.st)):
            if self.st[i].isalpha() or (
                    self.st[i] == '@' and i != len(self.st) - 1 and self.st[i + 1] not in self.punctuation) \
                    or (self.st[i] == "'" and i != len(self.st) - 1 and self.st[i + 1] not in self.punctuation):
                self.valids.append(self.st[i])
            if self.st[i] in self.punctuation and len(self.valids) != 0 and self.valids[-1] != ' ' and i != len(
                    self.st) - 1:
                self.valids.append(' ')
        return ''.join(self.valids).strip()

    # Расчет эмоциональной оценки для очищенной строки
    def sentiment_count(self, st):
        self.score = 0
        l = st.split()
        i = 0
        while i < len(l):
            f = 0
            if i == len(l) - 1:
                if l[i] in self.lexicon:
                    self.score += self.lexicon[l[i]]
                break
            for j in range(len(l) - 1, i - 1, -1):
                candidate = ' '.join(l[i:j + 1])
                if candidate in self.lexicon:
                    self.score += self.lexicon[candidate]
                    i += len(candidate.split())
                    f = 1
                    break
            if f == 0:
                i += 1
        return self.score

    # Расчет эмоциональной окраски сообщения для каждой строки
    # Занесение оценки эмоциональной окраски сообщения в БД
    def sentiment_count_to_db(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        for row in cur.execute('SELECT tweet_text FROM tweets_db_normalized'):
            s = self.clear_str(row[0])
            self.tweet_sentiments[row[0]] = self.sentiment_count(s)

        for row in self.tweet_sentiments:
            cur.execute('UPDATE tweets_db_normalized '
                        'SET tweet_sentiment = (?) '
                        'WHERE tweet_text = (?)',
                        (self.tweet_sentiments[row], row))

        con.commit()
        con.close()


sc = SentimentCount('AFINN-111.txt', 'tweets.db')
sc.sentiment_count_to_db()
