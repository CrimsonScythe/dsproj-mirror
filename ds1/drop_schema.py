import psycopg2

drop_query = """
DROP TABLE IF EXISTS Written_by CASCADE;
DROP TABLE IF EXISTS Tags CASCADE;
DROP TABLE IF EXISTS Webpage CASCADE;
DROP TABLE IF EXISTS Article CASCADE;
DROP TABLE IF EXISTS Article_type;
DROP TABLE IF EXISTS Type CASCADE;
DROP TABLE IF EXISTS Domain CASCADE;
DROP TABLE IF EXISTS Author CASCADE;
DROP TABLE IF EXISTS Keyword CASCADE;
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
