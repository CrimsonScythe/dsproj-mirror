INSERT INTO tags
SELECT article.article_id, keyword.keyword_id FROM article INNER JOIN keyword ON
article.meta_keywords=keyword.keyword
WHERE keyword.keyword != 'NULL';

SELECT * FROM tags;