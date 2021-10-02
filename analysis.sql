-- Наиболее счастливые страны
WITH avg_sentiments AS (
    SELECT DISTINCT country_code,
                    AVG(tweet_sentiment) OVER (PARTITION BY country_code) AVG_Hapiness
      FROM tweets_db_normalized
     WHERE country_code IS NOT NULL
)
SELECT country_code,
       AVG_Hapiness
  FROM avg_sentiments
 WHERE AVG_Hapiness = (
                          SELECT MAX(AVG_Hapiness) 
                            FROM avg_sentiments
                      ); 

-- Наименее счастливые страны
WITH avg_sentiments AS (
    SELECT DISTINCT country_code,
                    AVG(tweet_sentiment) OVER (PARTITION BY country_code) AVG_Hapiness
      FROM tweets_db_normalized
     WHERE country_code IS NOT NULL
)
SELECT country_code,
       AVG_Hapiness
  FROM avg_sentiments
 WHERE AVG_Hapiness = (
                          SELECT MIN(AVG_Hapiness) 
                            FROM avg_sentiments
                      );

-- Наиболее счастливые локации
WITH avg_sentiments AS (
    SELECT DISTINCT location,
                    AVG(tweet_sentiment) OVER (PARTITION BY location) AVG_Hapiness
      FROM tweets_db_normalized tbn
           JOIN
           locations l ON tbn.id = l.id
     WHERE location IS NOT NULL
)
SELECT location,
       AVG_Hapiness
  FROM avg_sentiments
 WHERE AVG_Hapiness = (
                          SELECT MAX(AVG_Hapiness) 
                            FROM avg_sentiments
                      );

-- Наименнее счастливые локации
WITH avg_sentiments AS (
    SELECT DISTINCT location,
                    AVG(tweet_sentiment) OVER (PARTITION BY location) AVG_Hapiness
      FROM tweets_db_normalized tbn
           JOIN
           locations l ON tbn.id = l.id
     WHERE location IS NOT NULL
)
SELECT location,
       AVG_Hapiness
  FROM avg_sentiments
 WHERE AVG_Hapiness = (
                          SELECT MIN(AVG_Hapiness) 
                            FROM avg_sentiments
                      );

-- Наиболее счастливые пользователи
WITH avg_sentiments AS (
    SELECT DISTINCT name,
                    tweet_text,
                    AVG(tweet_sentiment) OVER (PARTITION BY name) AVG_Hapiness
      FROM tweets_db_normalized
     WHERE name IS NOT NULL
)
SELECT name,
       tweet_text,
       AVG_Hapiness
  FROM avg_sentiments
 WHERE AVG_Hapiness = (
                          SELECT MAX(AVG_Hapiness) 
                            FROM avg_sentiments
                      );

-- Наименнее счастливые пользователи
WITH avg_sentiments AS (
    SELECT DISTINCT name,
                    tweet_text,
                    AVG(tweet_sentiment) OVER (PARTITION BY name) AVG_Hapiness
      FROM tweets_db_normalized
     WHERE name IS NOT NULL
)
SELECT name,
       tweet_text,
       AVG_Hapiness
  FROM avg_sentiments
 WHERE AVG_Hapiness = (
                          SELECT MIN(AVG_Hapiness) 
                            FROM avg_sentiments
                      );
       


     







