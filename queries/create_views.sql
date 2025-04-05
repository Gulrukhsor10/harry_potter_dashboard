-- 1. Топ-10 самых активных персонажей по количеству реплик
CREATE OR REPLACE VIEW most_active_characters AS
SELECT 
    Character,
    COUNT(*) AS num_quotes
FROM quotes
GROUP BY Character
ORDER BY num_quotes DESC
LIMIT 10;


-- 2. Топ-10 заклинаний по частоте упоминаний (по полю Name в quotes.Sentence)
CREATE OR REPLACE VIEW most_common_spells AS
SELECT 
    s.Name AS spell_name,
    COUNT(*) AS mention_count
FROM quotes q
JOIN spells s
    ON LOWER(q.Sentence) LIKE '%' || LOWER(s.Name) || '%'
GROUP BY s.Name
ORDER BY mention_count DESC
LIMIT 10;


-- 3. Заклинания, применённые главными персонажами (по соответствию Character и содержанию заклинания в Sentence)
CREATE OR REPLACE VIEW spells_used_by_main_characters AS
SELECT 
    q.Character,
    s.Name AS spell_name,
    COUNT(*) AS usage_count
FROM quotes q
JOIN spells s
    ON LOWER(q.Sentence) LIKE '%' || LOWER(s.Name) || '%'
WHERE q.Character IN ('Harry Potter', 'Hermione Granger', 'Ron Weasley', 'Albus Dumbledore', 'Lord Voldemort')
GROUP BY
