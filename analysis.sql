-- Наиболее счастливые страны (по коду страны), локация и пользователь, общая таблица
SELECT country_code Most_happy_country,
       location Most_happy_location,
       name Most_happy_user,
       tweet_text Most_happy_tweet,
       tweet_sentiment AFINN_sentiment
  FROM tweets_db_normalized tbn
       JOIN
       locations l ON tbn.id = l.id
 WHERE tweet_sentiment = (
                             SELECT MAX(tweet_sentiment) 
                               FROM tweets_db_normalized
                         );


-- Наименее счастливые страны (по коду страны), локация и пользователь, общая таблица
SELECT country_code Least_happy_country,
       location Least_happy_location,
       name Least_happy_user,
       tweet_text Least_happy_tweet,
       tweet_sentiment AFINN_sentiment
  FROM tweets_db_normalized tbn
       JOIN
       locations l ON tbn.id = l.id
 WHERE tweet_sentiment = (
                             SELECT MIN(tweet_sentiment) 
                               FROM tweets_db_normalized
                         );


-- Наиболее счастливая локация
SELECT location,
       tweet_sentiment
  FROM tweets_db_normalized tbn
       JOIN
       locations l ON tbn.id = l.id
 WHERE tweet_sentiment = (
                             SELECT MAX(tweet_sentiment) 
                               FROM tweets_db_normalized
                         )
AND 
       location IS NOT NULL
 ORDER BY location;



 
-- Наименнее счастливая локация
SELECT location,
       tweet_sentiment
  FROM tweets_db_normalized tbn
       JOIN
       locations l ON tbn.id = l.id
 WHERE tweet_sentiment = (
                             SELECT MIN(tweet_sentiment) 
                               FROM tweets_db_normalized
                         )
AND 
       location IS NOT NULL
 ORDER BY location;



-- Наиболее счастливые пользователи
SELECT name,
       tweet_text,
       tweet_sentiment
  FROM tweets_db_normalized
 WHERE tweet_sentiment = (
                             SELECT MAX(tweet_sentiment) 
                               FROM tweets_db_normalized
                         )
AND 
       name IS NOT NULL
 ORDER BY name;


-- Наименнее счастливые пользователи
SELECT name,
       tweet_text,
       tweet_sentiment
  FROM tweets_db_normalized
 WHERE tweet_sentiment = (
                             SELECT MIN(tweet_sentiment) 
                               FROM tweets_db_normalized
                         )
AND 
       name IS NOT NULL
 ORDER BY name;

