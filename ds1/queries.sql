-- 1.
-- WITH res AS (SELECT article_id FROM article INNER JOIN article_type ON
-- article.article_id=article_type.type_id
-- WHERE type_name='reliable' AND scraped_at>='2018-01-15 00:00:00.000000'::date)
-- SELECT domain.domain_url FROM domain INNER JOIN res ON
-- res.article_id=domain.domain_id;


-- 1. VERSION 2 WORKS WITH THE NEW DB 
WITH res AS (SELECT article_id FROM article WHERE scraped_at>='2018-01-15 00:00:00.000000'::date),
res2 AS (
	SELECT is_type.article_id
	FROM is_type INNER JOIN res 
	ON res.article_id=is_type.article_id
	WHERE is_type.type_id =
		(SELECT article_type.type_id
		 FROM article_type
		 WHERE type_name='reliable'
		)
)
SELECT domain.domain_url FROM domain WHERE domain.domain_id IN
(SELECT domain_id FROM webpage INNER JOIN res2 ON webpage.article_id=res2.article_id);

--1. ANOTHER VERSION ALSO works. Easier to convert to relational algebra:
SELECT DISTINCT domain.domain_url FROM domain NATURAL JOIN (SELECT webpage.article_id,webpage.domain_id FROM 
article NATURAL JOIN is_type NATURAL JOIN webpage
WHERE article.scraped_at>='2018-01-15 00:00:00.000000'::date
AND is_type.type_id=(SELECT type_id FROM article_type WHERE type_name='reliable')
) AS foo;


-- 2.
-- List the name(s) of the most prolific author(s) of news articles of fake type. 
-- An author is among the most prolific if it has authored as many or more fake 
-- news articles as any other author in the dataset. 
-- Languages: extended relational algebra and SQL

-- we have to join together so we have article id, type_id and author_id together.

SELECT count, author_name FROM (
	SELECT COUNT(article_id), author_id FROM (
		SELECT Written_by.article_id, Written_by.author_id FROM Written_by
		INNER JOIN Is_type
		ON Written_by.article_id = Is_type.article_id
		WHERE Is_type.type_id = 27
		) AS articles_authored_by
	GROUP BY author_id
	ORDER BY COUNT(article_id) DESC
	) AS articles_authored_by_ordered_desc
INNER JOIN Author
ON articles_authored_by_ordered_desc.author_id = Author.author_id
ORDER BY count DESC


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
-- SELECT COUNT (article_id), keyword_id 
-- FROM (
-- SELECT * FROM tags
-- WHERE tags.keyword_id != (SELECT keyword.keyword_id FROM
--  keyword WHERE keyword.keyword = 'NULL')
-- ) AS foo
-- GROUP BY keyword_id
-- ORDER BY COUNT(article_id) DESC;
-- VRESION 4
WITH res AS (SELECT DISTINCT
LEAST(t1.article_id, t2.article_id), t1.keyword_id L1key,
GREATEST(t1.article_id, t2.article_id), t2.keyword_id L2 FROM
tags AS t1 CROSS JOIN tags AS t2
WHERE t1.article_id!=t2.article_id AND t1.keyword_id=t2.keyword_id 
			 AND t1.keyword_id != (SELECT keyword.keyword_id FROM
 keyword WHERE keyword.keyword = 'NULL') AND t2.keyword_id != (SELECT keyword.keyword_id FROM
 keyword WHERE keyword.keyword = 'NULL'))
SELECT COUNT(least),L1key FROM res
GROUP BY L1key
ORDER BY COUNT(least) DESC;
