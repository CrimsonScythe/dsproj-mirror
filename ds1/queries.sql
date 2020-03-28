-- 1.
WITH res AS (SELECT article_id FROM article INNER JOIN article_type ON
article.article_id=article_type.type_id
WHERE type_name='reliable' AND scraped_at>='2018-01-15 00:00:00.000000'::date)
SELECT domain.domain_url FROM domain INNER JOIN res ON
res.article_id=domain.domain_id;
-- 2.
SELECT COUNT(author_name), author_name FROM author INNER JOIN article_type ON
author.author_id=article_type.type_id WHERE 
article_type.type_name='fake' AND NOT author_name=''
GROUP BY author_name
ORDER BY COUNT(author_name) DESC;
--3. 
-- VERSION 1: (deprecated)
-- SELECT COUNT(article_id), meta_keywords FROM article
-- WHERE NOT meta_keywords='[]' AND NOT meta_keywords='[ ]'
-- GROUP BY meta_keywords
-- ORDER BY COUNT(article_id) DESC;
-- VERSION 2: (also deprecated)
-- SELECT COUNT (article_id), keyword_id FROM tags
-- GROUP BY keyword_id
-- ORDER BY COUNT(article_id) DESC

-- VERSION 3: (in prod :D)
-- Needed to update this query since meta_keywords from article table cannot be used.
-- Thus, here we use the tags and keywords table to find the required info.
SELECT COUNT (article_id), keyword_id 
FROM (
SELECT * FROM tags
WHERE tags.keyword_id != (SELECT keyword.keyword_id FROM keyword WHERE keyword.keyword = 'NULL')
) AS foo
GROUP BY keyword_id
ORDER BY COUNT(article_id) DESC;
