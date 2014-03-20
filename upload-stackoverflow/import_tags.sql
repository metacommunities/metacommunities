-- define tag table
CREATE TABLE tags (
  id INTEGER PRIMARY KEY,
  tag TEXT NULL,
  count INTEGER NULL,
  count_gte10 BOOLEAN NULL,
  count_gte50 BOOLEAN NULL,
  INDEX id (id),
  INDEX tag (tag (10))
)
CHARACTER SET utf8
COLLATE utf8_general_ci;

-- load tag data
LOAD DATA LOCAL INFILE 'stackoverflow.com/Tags.csv' INTO TABLE tags
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, tag);

-- define posttag table
CREATE TABLE posttags (
  pid INTEGER,
  tid INTEGER.
  INDEX pid (pid),
  INDEX tid (tid)  
)
CHARACTER SET utf8
COLLATE utf8_general_ci;

-- load_posttag data
LOAD DATA LOCAL INFILE 'stackoverflow.com/PostTags.csv' INTO TABLE posttags
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

-- count tags
UPDATE tags
SET count = (
  SELECT count(*)
  FROM posttags
  WHERE tags.id = posttags.tid
);

-- identify counts greater than or equal to 10
UPDATE tags SET count_gte10 = 1 WHERE count >= 10;
ALTER TABLE tags ADD INDEX count_gte10 (count_gte10);

-- identify counts greater than or equal to 50
UPDATE tags SET count_gte50 = 1 WHERE count >= 50;
ALTER TABLE tags ADD INDEX count_gte50 (count_gte50);

-- "interesting" posttags
CREATE TABLE posttag_gte10
AS
SELECT pid, tid
FROM posttags
WHERE tid IN (
  SELECT id
  FROM tags
  WHERE count_gte10 = 1
);

ALTER TABLE posttag_gte10 ADD INDEX pid (pid);
ALTER TABLE posttag_gte10 ADD INDEX tid (tid);

CREATE TABLE posttag_gte50
AS
SELECT pid, tid
FROM posttags
WHERE tid IN (
  SELECT id
  FROM tags
  WHERE count_gte50 = 1
);

ALTER TABLE posttag_gte50 ADD INDEX pid (pid);
ALTER TABLE posttag_gte50 ADD INDEX tid (tid);

