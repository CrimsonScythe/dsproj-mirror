DROP TABLE IF EXISTS Written_by CASCADE;
DROP TABLE IF EXISTS Tags CASCADE;
DROP TABLE IF EXISTS Webpage CASCADE;
DROP TABLE IF EXISTS Article CASCADE;
DROP TABLE IF EXISTS Article_type;
DROP TABLE IF EXISTS Type CASCADE;
DROP TABLE IF EXISTS Domain CASCADE;
DROP TABLE IF EXISTS Author CASCADE;
DROP TABLE IF EXISTS Keyword CASCADE;

CREATE TABLE Keyword (
  keyword_id serial,
  keyword varchar,
  PRIMARY KEY (keyword_id)
);

CREATE TABLE Author (
  author_id serial,
  author_name varchar,
  PRIMARY KEY (author_id)
);

CREATE TABLE Domain (
  domain_id serial,
  domain_url varchar,
  PRIMARY KEY (domain_id)
);

CREATE TABLE Article_type (
  type_id serial,
  type_name varchar(64),
  PRIMARY KEY (type_id)
);

CREATE TABLE Article (
  article_id integer,
  title varchar,
  content text,
  summary text,
  written_by text,
  type_id integer REFERENCES Article_type(type_id),
  meta_description text,
  meta_keywords text,
  inserted_at timestamp,
  updated_at timestamp,
  scraped_at timestamp,
  PRIMARY KEY (article_id)
);

CREATE TABLE Webpage (
  url varchar,
  article_id integer REFERENCES Article(article_id),
  domain_id integer REFERENCES Domain(domain_id)
);

CREATE TABLE Tags (
  article_id integer REFERENCES Article(article_id),
  keyword_id integer REFERENCES Keyword(keyword_id)
);


-- Made part of Article instead
--CREATE TABLE Written_by (
--article_id integer REFERENCES Article(article_id),
--author_id integer REFERENCES Author(author_id)
--);


