import psycopg2

create_query = """
CREATE TABLE wikinews.Keyword (
  keyword_id serial,
  keyword varchar,
  PRIMARY KEY (keyword_id)
);

CREATE TABLE wikinews.Author (
  author_id serial,
  author_name varchar,
  PRIMARY KEY (author_id)
);

CREATE TABLE wikinews.Domain (
  domain_id serial,
  domain_url varchar,
  PRIMARY KEY (domain_id)
);

CREATE TABLE wikinews.Article_type (
  type_id serial,
  type_name varchar,
  PRIMARY KEY (type_id)
);

CREATE TABLE wikinews.Article (
  article_id integer,
  title varchar,
  content text,
  summary text,
  meta_description text,
  inserted_at timestamp,
  updated_at timestamp,
  scraped_at timestamp,
  meta_keywords text,
  PRIMARY KEY (article_id)
);

CREATE TABLE wikinews.Webpage (
  article_id integer REFERENCES wikinews.Article(article_id),
  domain_id integer REFERENCES wikinews.Domain(domain_id),
  url text
);

CREATE TABLE wikinews.Tags (
  article_id integer REFERENCES wikinews.Article(article_id),
  keyword_id integer REFERENCES wikinews.Keyword(keyword_id)
);

CREATE TABLE wikinews.is_type (
   article_id integer REFERENCES wikinews.Article(article_id),
   type_id integer REFERENCES wikinews.article_type(type_id)
);

CREATE TABLE wikinews.written_by (
  article_id integer REFERENCES wikinews.Article(article_id),
  author_id integer REFERENCES wikinews.Author(author_id)
);
"""

conn = psycopg2.connect(
  host = "localhost",
  dbname="postgres",
  user="postgres",
  password="root")
cur = conn.cursor() 
cur.execute(create_query)
conn.commit()
cur.close()
