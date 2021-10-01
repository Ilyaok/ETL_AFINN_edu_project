# Методика расчета AFINN: http://www2.imm.dtu.dk/pubdb/edoc/imm6975.pdf
# В задании не уточнено, следует ли использовать библиотеку, https://github.com/fnielsen/afinn
# Исходя из формулировки задания принято решение написать скрипт на основе AFINN самостоятельно

import sqlite3


class SentimentCount:

    def __init__(self, afinn_path, db_path):
        self.afinn_path = afinn_path
        self.db_path = db_path
        self.valids = []
        self.lexicon = {}
        self.score = 0
        self.st = []
        self.tweet_sentiments = {}

    # Перевод строки в нижний регистр и оставление в ней только буквенных символов
    # todo добавить обработку случаев "abc,efgh', 'abcd!', ссылок 'http://' и др.
    # todo перепроверить пробелы и табуляции, а также другие символы разделения
    # todo оптимизировать работу с twitter-никами
    def clear_str(self, st):
        self.st = st.lower().strip()
        self.valids = []
        for c in self.st:
            if c.isalpha() or c == ' ' or c == '_' or c == '@':
                self.valids.append(c)
        return ''.join(self.valids)

    # Расчет эмоциональной оценки для очищенной строки
    def sentiment_count(self, st):
        self.score = 0
        for c in st.split():
            if c in self.lexicon:
                self.score += self.lexicon[c]
        return self.score

    # Расчет эмоциональной окраски сообщения для каждой строки
    # Занесение оценки эмоциональной окраски сообщения в БД
    def sentiment_count_to_db(self):
        # Создание словаря из файла AFINN-111.txt
        with open(self.afinn_path) as f:
            for line in f:
                self.lexicon[' '.join(line.split()[:-1])] = int(line.split()[-1])

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
