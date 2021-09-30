-- Поле root -> id в изначальном json не содержит уникальных значений, поэтому принято решение  сделать отдельное поле tweet_id в качестве Первичного ключа
-- Поле location в json лежит в директории user, соответственно, зависит от поля name, поэтому выносим зависимость name-location в отдельную таблицу
-- Остальные поля зависят напрямую от id твита, поэтому не подлежат нормализации

-- Добавление id твита
PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM tweets_db;

DROP TABLE tweets_db;

CREATE TABLE tweets_db (
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

INSERT INTO tweets_db (
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
                        FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;


-- Создание таблицы locations и внесение в нее данных
CREATE TABLE locations (
    id        INTEGER  PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR,
    location        VARCHAR,
    FOREIGN KEY (id) REFERENCES tweets_db(id)
);

INSERT INTO locations (
                          id,
                          name,
                          location
                      )
                      SELECT id,
                             name, 
                             location
                        FROM tweets_db;
                        

-- Удаление поля location из таблицы tweets_db
PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM tweets_db;

DROP TABLE tweets_db;

CREATE TABLE tweets_db (
    id        INTEGER  PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR,
    tweet_text      VARCHAR,
    country_code    VARCHAR,
    display_url     VARCHAR,
    lang            VARCHAR,
    created_at      DATETIME,
    tweet_sentiment INT      DEFAULT (0) 
);

INSERT INTO tweets_db (
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




