-- define tag table
CREATE TABLE tag (
  id INTEGER PRIMARY KEY,
  tag TEXT NULL,
  count INTEGER NULL,
  count_gte10 BOOLEAN NULL,
  count_gte50 BOOLEAN NULL
)
CHARACTER SET utf8
COLLATE utf8_general_ci;

-- load tag data
LOAD DATA LOCAL INFILE 'stackoverflow.com/Tags.csv' INTO TABLE tag
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, tag);

ALTER TABLE tag ADD UNIQUE INDEX id (id);
ALTER TABLE tag ADD UNIQUE INDEX tag (tag (10));

-- define posttag table
CREATE TABLE posttag (
  pid INTEGER,
  tid INTEGER
)
CHARACTER SET utf8
COLLATE utf8_general_ci;

-- load_posttag data
LOAD DATA LOCAL INFILE 'stackoverflow.com/PostTags.csv' INTO TABLE posttag
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

ALTER TABLE posttag ADD INDEX pid (pid);
ALTER TABLE posttag ADD INDEX tid (tid);

-- count tags
UPDATE tag
SET count = (
  SELECT count(*)
  FROM posttag
  WHERE tag.id = posttag.tid
);

-- identify counts greater than or equal to 10
UPDATE tag SET count_gte10 = 1 WHERE count >= 10;
ALTER TABLE tag ADD INDEX count_gte10 (count_gte10);

-- identify counts greater than or equal to 50
UPDATE tag SET count_gte50 = 1 WHERE count >= 50;
ALTER TABLE tag ADD INDEX count_gte50 (count_gte50);

-- "interesting" posttags
CREATE TABLE posttag_gte10
AS
SELECT pid, tid
FROM posttag
WHERE tid IN (
  SELECT id
  FROM tag
  WHERE count_gte10 = 1
);

ALTER TABLE posttag_gte10 ADD INDEX pid (pid);
ALTER TABLE posttag_gte10 ADD INDEX tid (tid);

CREATE TABLE posttag_gte50
AS
SELECT pid, tid
FROM posttag
WHERE tid IN (
  SELECT id
  FROM tag
  WHERE count_gte50 = 1
);

ALTER TABLE posttag_gte50 ADD INDEX pid (pid);
ALTER TABLE posttag_gte50 ADD INDEX tid (tid);

