
1. Написать скрипт на Python который загружает в БД (sqlite3) данные по каждому твиту из файла “three_minutes_tweets.json.txt”:
структура твита: name, tweet_text, country_code, display_url, lang, created_at, location

2. Для каждого твита в базе необходимо завести атрибут с эмоциональной оценкой сообщения: tweet_sentiment

3. Подумать как можно нормализовать хранение твита (привести SQL-скрипты создания/изменения нормализованной структуры данных)

4. Написать скрипт на Python для подсчета среднего sentiment (Эмоциональной окраски сообщения) на основе AFINN-111.txt и заполнить  для каждого твита tweet_sentiment колонку. 
Если твит не содержит слов из словаря то предполагать что sentiment = 0

AFINN ReadMe:

AFINN is a list of English words rated for valence with an integer
between minus five (negative) and plus five (positive). The words have
been manually labeled by Finn Arup Nielsen in 2009-2011. The file
is tab-separated. There are two versions:
AFINN-111: Newest version with 2477 words and phrases.

5. Написать SQL скрипт, который выводит наиболее и наименее счастливую страну, локацию и пользователя (дял пользователя - вместе с его твитами), предоставить сами скрипты и результаты их работы.

6. Описать свое видение решения, которое позволит выполнять ежедневно анализ согласно п.5. Из каких компонентов должно состоять решение, из каких шагов должен состоять ETL процесс от обработки входящих файлов до этапа сохранения конечной информации.
- на входе - непрерывный поток на FTP твитов в файлах (tweet.json), с частотой каждые три минуты. Размеры файлов - в среднем x10 от предоставленного сэмпла.
- на выходе - пользователи должны иметь возможность анализировать счастье по странам, локациям, пользователям, отслеживать изменения, собирать статиcтику и т.д. 
