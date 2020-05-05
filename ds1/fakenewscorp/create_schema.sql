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
  type_name varchar,
  PRIMARY KEY (type_id)
);

CREATE TABLE Article (
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

CREATE TABLE Webpage (
  article_id integer REFERENCES Article(article_id),
  domain_id integer REFERENCES Domain(domain_id),
  url text
);

CREATE TABLE Tags (
  article_id integer REFERENCES Article(article_id),
  keyword_id integer REFERENCES Keyword(keyword_id)
);

CREATE TABLE is_type (
   article_id integer REFERENCES Article(article_id),
   type_id integer REFERENCES article_type(type_id)
);