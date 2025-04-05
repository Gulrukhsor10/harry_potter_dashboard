-- Пример: все персонажи с факультетом
SELECT Name, House
FROM characters
WHERE House IS NOT NULL;

-- Пример: общее число заклинаний по типам
SELECT Type, COUNT(*) AS count
FROM spells
GROUP BY Type
ORDER BY count DESC;

-- Пример: длина реплик по персонажам (только активные)
SELECT 
    Character,
    AVG(LENGTH(Sentence)) AS avg_length
FROM quotes
GROUP BY Character
HAVING COUNT(*) > 20
ORDER BY avg_length DESC
LIMIT 10;

-- Пример: частота использования заклинания "Accio"
SELECT 
    COUNT(*) AS accio_count
FROM quotes
WHERE LOWER(Sentence) LIKE '%accio%';
