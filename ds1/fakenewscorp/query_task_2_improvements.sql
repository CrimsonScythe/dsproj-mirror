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

-- In line 9, replace COUNT(article_id) with count. Seems to, on average, not really make any difference. Might be faster with 50 ms, but. 

SELECT count, author_name FROM (
	SELECT COUNT(article_id), author_id FROM (
		SELECT Written_by.article_id, Written_by.author_id FROM Written_by
		INNER JOIN Is_type
		ON Written_by.article_id = Is_type.article_id
		WHERE Is_type.type_id = 27
		) AS articles_authored_by
	GROUP BY author_id
	ORDER BY count DESC
	) AS articles_authored_by_ordered_desc
INNER JOIN Author
ON articles_authored_by_ordered_desc.author_id = Author.author_id
ORDER BY count DESC