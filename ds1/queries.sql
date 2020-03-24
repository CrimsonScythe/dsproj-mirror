-- 1.
WITH res AS (SELECT article_id FROM article INNER JOIN article_type ON
article.article_id=article_type.type_id
WHERE type_name='reliable' AND scraped_at>='2018-01-15 00:00:00.000000'::date)
SELECT domain.domain_url FROM domain INNER JOIN res ON
res.article_id=domain.domain_id
-- 2.
SELECT COUNT(author_name), author_name FROM author INNER JOIN article_type ON
author.author_id=article_type.type_id WHERE 
article_type.type_name='fake' AND NOT author_name=''
GROUP BY author_name
ORDER BY COUNT(author_name) DESC;
--3. 
SELECT COUNT(article_id), meta_keywords FROM article
WHERE NOT meta_keywords='[]' AND NOT meta_keywords='[ ]'
GROUP BY meta_keywords
ORDER BY COUNT(article_id) DESC;
