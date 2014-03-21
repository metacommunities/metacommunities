CREATE TEMPORARY TABLE numbers (
  n INT PRIMARY KEY
);

INSERT INTO numbers VALUES (2),(3),(4),(5),(6);


DROP TABLE IF EXISTS tags;

CREATE TABLE tags (
  pid   INTEGER,
  tag   TINYTEXT,
  INDEX tag (tag (5))
);


-- 'insertTagsPage' procedure
-- for a certain LIMIT and OFFSET it will process the tags field in the
-- posts table and output it into the tags table
CREATE PROCEDURE insertTagsPage
(
  page_limit INT,
  offset_by INT
) 
  INSERT INTO tags (pid, tag)
    SELECT
      subposts.id AS pid,
      SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING_INDEX(subposts.tags, '<', numbers.n), '<', -1), '>', 1) AS tag
    FROM
      numbers
      INNER JOIN (
        SELECT id, tags
        FROM posts
        LIMIT page_limit OFFSET offset_by
      ) AS subposts
        ON (CHAR_LENGTH(subposts.tags) - CHAR_LENGTH(REPLACE(subposts.tags, '<', ''))) >= (numbers.n - 1)
    ORDER BY
      pid, n;


-- insertTags procedure
-- process 1 million posts at a time, sending each batch to insertTagsPage
DELIMITER $$
CREATE PROCEDURE insertTags ()
BEGIN
  -- parameters for paging insert statement
  SET @i = 0;
  SET @page_limit = 1000000;
  SELECT count(*) INTO @posts_count FROM posts;  

  -- start
  WHILE @i < @posts_count
  DO
    CALL insertTagsPage(@page_limit, @i);
    SET @i = @i + @page_limit;
  END WHILE;
END$$
DELIMITER ;


-- go
LOCK TABLES posts READ, numbers READ, tags WRITE;

CALL insertTags();

UNLOCK TABLES;
UNLOCK TABLES;

