import psycopg2

queries = [
"""
CREATE TABLE fakenewscorp.Keyword (
  keyword_id serial,
  keyword varchar,
  PRIMARY KEY (keyword_id)
);
""",
"""
CREATE TABLE fakenewscorp.Author (
  author_id serial,
  author_name varchar,
  PRIMARY KEY (author_id)
);
""",
"""
CREATE TABLE fakenewscorp.Domain (
  domain_id serial,
  domain_url varchar,
  PRIMARY KEY (domain_id)
);
""",
"""
CREATE TABLE fakenewscorp.Article_type (
  type_id serial,
  type_name varchar,
  PRIMARY KEY (type_id)
);
""",
"""
CREATE TABLE fakenewscorp.Article (
  article_id integer,
  title varchar,
  content text,
  summary text,
  --written_by text,
  -- type_id integer REFERENCES Article_type(type_id),
  meta_description text,
  inserted_at timestamp,
  updated_at timestamp,
  scraped_at timestamp,
  meta_keywords text,
  PRIMARY KEY (article_id)
);
""",
"""
CREATE TABLE fakenewscorp.Webpage (
  article_id integer REFERENCES Article(article_id),
  domain_id integer REFERENCES Domain(domain_id),
  url text
);
""",
"""
CREATE TABLE fakenewscorp.tags (
  article_id integer REFERENCES Article(article_id),
  keyword_id integer REFERENCES Keyword(keyword_id)
);
""",
"""
CREATE TABLE fakenewscorp.is_type (
   article_id integer REFERENCES Article(article_id),
   type_id integer REFERENCES article_type(type_id)
);
""",
"""
CREATE TABLE fakenewscorp.written_by (
  article_id integer REFERENCES Article(article_id),
  author_id integer REFERENCES Author(author_id)
);
"""]

conn = psycopg2.connect(
  host = "localhost",
  dbname="postgres",
  user="postgres",
  password="root")
cur = conn.cursor()
for query in queries:
  try:
    cur.execute(query)
    conn.commit()
  except:
    conn.commit()
cur.close()
