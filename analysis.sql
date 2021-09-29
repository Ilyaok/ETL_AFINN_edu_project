-- Наиболее счастливая локация
SELECT location,
       tweet_sentiment
  FROM tweets_db
 WHERE tweet_sentiment = (
                             SELECT MAX(tweet_sentiment) 
                               FROM tweets_db
                         )
AND 
       location IS NOT NULL
 ORDER BY location;


 
-- Наименнее счастливая локация
SELECT location,
       tweet_sentiment
  FROM tweets_db
 WHERE tweet_sentiment = (
                             SELECT MIN(tweet_sentiment) 
                               FROM tweets_db
                         )
AND 
       location IS NOT NULL
 ORDER BY location;



-- Наиболее счастливые пользователи
SELECT name,
       tweet_text,
       tweet_sentiment
  FROM tweets_db
 WHERE tweet_sentiment = (
                             SELECT MAX(tweet_sentiment) 
                               FROM tweets_db
                         )
AND 
       name IS NOT NULL
 ORDER BY name;



 
-- Наименнее счастливые пользователи
SELECT name,
       tweet_text,
       tweet_sentiment
  FROM tweets_db
 WHERE tweet_sentiment = (
                             SELECT MIN(tweet_sentiment) 
                               FROM tweets_db
                         )
AND 
       name IS NOT NULL
 ORDER BY name;

