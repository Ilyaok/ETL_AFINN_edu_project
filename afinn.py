# Методика расчета AFINN: http://www2.imm.dtu.dk/pubdb/edoc/imm6975.pdf
# В задании не уточнено, следует ли использовать библиотеку, https://github.com/fnielsen/afinn
# Исходя из формулировки задания принято решение написать скрипт на основе AFINN самостоятельно

import sqlite3

# Создание словаря из файла AFINN-111.txt
lexicon = {}
with open('AFINN-111.txt') as f:
    for line in f:
        lexicon[' '.join(line.split()[:-1])] = int(line.split()[-1])

con = sqlite3.connect('tweets.db')
cur = con.cursor()

tweet_sentiments = {}


# Перевод строки в нижний регистр и оставление в ней только буквенных символов
# todo добавить обработку случаев "abc,efgh', 'abcd!', ссылок 'http://' и др.
# todo перепроверить пробелы и табуляции, а также другие символы разделения
# todo оптимизировать работу с twitter-никами
def clear_str(s_input):
    valids = []
    s = s_input.lower().strip()
    for c in s:
        if c.isalpha() or c == ' ' or c == '_' or c == '@':
            valids.append(c)
    return ''.join(valids)


# Расчет эмоциональной оценки для очищенной строки
# todo детальная проверка (юнит-тестирование) работы ф-ции
def sentiment_count(st, lex):
    score = 0
    l = st.split()
    for c in l:
        if c in lex:
            score += lex[c]
    return score


# Расчет эмоциональной окраски сообщения
for row in cur.execute('SELECT tweet_text FROM tweets_db_normalized'):
    s = clear_str(row[0])
    tweet_sentiments[row[0]] = sentiment_count(s, lexicon)

for row in tweet_sentiments:
    cur.execute('UPDATE tweets_db_normalized '
                'SET tweet_sentiment = (?) '
                'WHERE tweet_text = (?)',
                (tweet_sentiments[row], row))

con.commit()
con.close()
