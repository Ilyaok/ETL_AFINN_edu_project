-- Поле root -> id в изначальном json не содержит уникальных значений, поэтому принято решение  сделать отдельное поле tweet_id в качестве Первичного ключа
-- Поле location в json лежит в директории user, соответственно, зависит от поля name, поэтому выносим зависимость name-location в отдельную таблицу
-- Остальные поля зависят напрямую от id твита, поэтому не подлежат нормализации



-- Создание нормализованной таблицы
CREATE TABLE IF NOT EXISTS tweets_db_normalized (
    id        INTEGER  PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR,
    tweet_text      VARCHAR,
    country_code    VARCHAR,
    display_url     VARCHAR,
    lang            VARCHAR,
    created_at      DATETIME,
    location        VARCHAR,
    tweet_sentiment INT      DEFAULT (0) 
);

INSERT INTO tweets_db_normalized (
                          name,
                          tweet_text,
                          country_code,
                          display_url,
                          lang,
                          created_at,
                          location,
                          tweet_sentiment
                      )
                      SELECT name,
                             tweet_text,
                             country_code,
                             display_url,
                             lang,
                             created_at,
                             location,
                             tweet_sentiment
                        FROM tweets_db;


-- Создание таблицы locations
CREATE TABLE IF NOT EXISTS locations (
    id        INTEGER  PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR,
    location        VARCHAR,
    FOREIGN KEY (id) REFERENCES tweets_db_normalized(id)
);

INSERT INTO locations (
                          id,
                          name,
                          location
                      )
                      SELECT id,
                             name, 
                             location
                        FROM tweets_db_normalized;


-- Удаление поля location из нормализованной таблицы
PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM tweets_db_normalized;

DROP TABLE tweets_db_normalized;

CREATE TABLE tweets_db_normalized (
    id        INTEGER  PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR,
    tweet_text      VARCHAR,
    country_code    VARCHAR,
    display_url     VARCHAR,
    lang            VARCHAR,
    created_at      DATETIME,
    tweet_sentiment INT      DEFAULT (0) 
);

INSERT INTO tweets_db_normalized (
                          id,
                          name,
                          tweet_text,
                          country_code,
                          display_url,
                          lang,
                          created_at,
                          tweet_sentiment
                      )
                      SELECT id,
                             name,
                             tweet_text,
                             country_code,
                             display_url,
                             lang,
                             created_at,
                             tweet_sentiment
                        FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;




