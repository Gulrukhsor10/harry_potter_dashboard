-- Создание таблицы characters
DROP TABLE IF EXISTS characters;
CREATE TABLE characters AS
SELECT * FROM read_csv_auto('source/Characters.csv', delim=';');

-- Создание таблицы spells
DROP TABLE IF EXISTS spells;
CREATE TABLE spells AS
SELECT * FROM read_csv_auto('source/Spells.csv', delim=';');

-- Создание таблицы potions
DROP TABLE IF EXISTS potions;
CREATE TABLE potions AS
SELECT * FROM read_csv_auto('source/Potions.csv', delim=';');

-- Создание таблицы quotes (объединение 3 файлов)
DROP TABLE IF EXISTS quotes;
CREATE TABLE quotes AS
SELECT * FROM (
    SELECT * FROM read_csv_auto('source/Harry Potter 1.csv', delim=';')
    UNION ALL
    SELECT * FROM read_csv_auto('source/Harry Potter 2.csv', delim=';')
    UNION ALL
    SELECT * FROM read_csv_auto('source/Harry Potter 3.csv', delim=';')
);
