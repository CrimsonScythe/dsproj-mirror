# Part II: ER-to-Relational Mapping

CREATE TABLE Article (
    article_id int PRIMARY KEY,
    summary VARCHAR,
    content VARCHAR,
    title varchar(255),
    inserted at DATETIME,
    scrapped at DATETIME,
    created ad DATETIME
);

CREATE TABLE written_By (
    author_id INT
    article_id INT
    PRIMARY KEY(article_id, author_id)
    FOREIGN KEY(article_id)

)
