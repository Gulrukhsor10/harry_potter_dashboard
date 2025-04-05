import streamlit as st
import plotly.express as px
from database import run_query  # импортируем из файла database.py

st.set_page_config(page_title="Гарри Поттер: Дашборд", layout="wide")
st.title("Дашборд по Гарри Поттеру")

st.markdown("Проект создан на основе анализа реплик, заклинаний и персонажей первых трёх фильмов.")

# Фильтры
houses = run_query("SELECT DISTINCT House FROM characters WHERE House IS NOT NULL AND House <> ''")
house_filter = st.selectbox("Выберите факультет", houses["House"].tolist())

min_quotes = st.slider("Минимальное количество реплик персонажа", min_value=0, max_value=50, value=10)

# График 1: Топ-10 говорящих в выбранном факультете
df1 = run_query(f"""
SELECT Name, COUNT(q.Sentence) AS num_quotes
FROM characters c
JOIN quotes q ON q.Character = c.Name
WHERE c.House = '{house_filter}'
GROUP BY Name
HAVING COUNT(q.Sentence) > {min_quotes}
ORDER BY num_quotes DESC
LIMIT 10
""")

st.plotly_chart(px.bar(df1, x="Name", y="num_quotes", title=f"Топ-10 говорящих в {house_filter}"), use_container_width=True)

# График 2: Топ-10 заклинаний по упоминаниям
df2 = run_query("""
SELECT 
    s.Name AS spell_name,
    COUNT(*) AS mentions
FROM quotes q
JOIN spells s ON LOWER(q.Sentence) LIKE '%' || LOWER(s.Name) || '%'
GROUP BY s.Name
ORDER BY mentions DESC
LIMIT 10
""")

st.plotly_chart(px.bar(df2, x="spell_name", y="mentions", title="Топ-10 заклинаний по упоминаниям"), use_container_width=True)

# График 3: Гарри против Волдеморта по фильмам
df3 = run_query("""
SELECT 
    CASE 
        WHEN file = 'Harry Potter 1.csv' THEN 'Фильм 1'
        WHEN file = 'Harry Potter 2.csv' THEN 'Фильм 2'
        WHEN file = 'Harry Potter 3.csv' THEN 'Фильм 3'
    END AS film,
    Character,
    COUNT(*) AS num_quotes
FROM (
    SELECT *, 'Harry Potter 1.csv' AS file FROM read_csv_auto('source/Harry Potter 1.csv', delim=';')
    UNION ALL
    SELECT *, 'Harry Potter 2.csv' AS file FROM read_csv_auto('source/Harry Potter 2.csv', delim=';')
    UNION ALL
    SELECT *, 'Harry Potter 3.csv' AS file FROM read_csv_auto('source/Harry Potter 3.csv', delim=';')
) q
WHERE Character IN ('Harry', 'Voldemort')
GROUP BY film, Character
ORDER BY film, Character
""")

st.plotly_chart(px.bar(df3, x="film", y="num_quotes", color="Character", barmode="group",
                       title="Гарри vs Волдеморт: количество реплик по фильмам"), use_container_width=True)

# График 4: Распределение длины реплик
df4 = run_query("""
SELECT LENGTH(Sentence) AS sentence_length
FROM quotes
WHERE LENGTH(Sentence) < 300
""")

st.plotly_chart(px.histogram(df4, x="sentence_length", nbins=40,
                              title="Распределение длины реплик"), use_container_width=True)
