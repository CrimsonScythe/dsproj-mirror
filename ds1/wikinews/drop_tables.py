import psycopg2

drop_query = """
DROP TABLE IF EXISTS wikinews.Written_by CASCADE;
DROP TABLE IF EXISTS wikinews.Tags CASCADE;
DROP TABLE IF EXISTS wikinews.Webpage CASCADE;
DROP TABLE IF EXISTS wikinews.Article CASCADE;
DROP TABLE IF EXISTS wikinews.Article_type CASCADE;
DROP TABLE IF EXISTS wikinews.Type CASCADE;
DROP TABLE IF EXISTS wikinews.Domain CASCADE;
DROP TABLE IF EXISTS wikinews.Author CASCADE;
DROP TABLE IF EXISTS wikinews.Keyword CASCADE;
DROP TABLE IF EXISTS wikinews.is_type CASCADE;
"""

conn = psycopg2.connect(
	host = "localhost",
	dbname="postgres",
	user="postgres",
	password="root")
cur = conn.cursor() 
cur.execute(drop_query)
conn.commit()
cur.close()
