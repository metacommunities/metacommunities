-- post
CREATE TABLE IF NOT EXISTS posts (
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
  ViewCount             INTEGER NULL,
  INDEX Id (Id),
  INDEX PostType (PostTypeId)
)
CHARACTER SET utf8
COLLATE utf8_general_ci
ENGINE = InnoDB;

LOAD XML LOCAL INFILE 'stackoverflow.com/stackoverflow.com-Posts' INTO TABLE posts
ROWS IDENTIFIED BY '<row>';
