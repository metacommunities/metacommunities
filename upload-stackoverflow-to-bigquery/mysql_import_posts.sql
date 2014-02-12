-- run this file by using something like:
-- mysql -u so_import -p -h localhost --local_infile=1 so < import_into_mysql.sql

-- define post table
CREATE TABLE post (
  AcceptedAnswerId      INTEGER NULL,
  AnswerCount           INTEGER NULL,
  Body                  LONGTEXT NULL,
  ClosedDate            TINYTEXT NULL,
  CommentCount          INTEGER NULL,
  CommunityOwnedDate    TINYTEXT NULL,
  CreationDate          TINYTEXT NULL,
  FavoriteCount         INTEGER NULL, 
  Id                    INTEGER NULL,
  LastActivityDate      TINYTEXT NULL,
  LastEditDate          TINYTEXT NULL,
  LastEditorDisplayName TINYTEXT NULL,
  LastEditorUserId      INTEGER NULL,
  OwnerDisplayName      TINYTEXT NULL,
  OwnerUserId           INTEGER NULL,
  ParentId              INTEGER NULL,
  PostTypeId            INTEGER NULL,
  Score                 INTEGER NULL,
  Tags                  TEXT NULL,
  Title                 TEXT NULL,
  ViewCount             INTEGER NULL
)
CHARACTER SET utf8
COLLATE utf8_general_ci;

-- load post data
LOAD XML LOCAL INFILE 'stackoverflow.com/Posts.xml' INTO TABLE post
ROWS IDENTIFIED BY '<row>';

ALTER TABLE post ADD UNIQUE INDEX Id (Id)
ALTER TABLE post ADD INDEX PostTypeId (PostTypeId)

