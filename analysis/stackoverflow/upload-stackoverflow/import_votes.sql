
CREATE TABLE IF NOT EXISTS votes (
  Id            INTEGER,
  PostId        INTEGER,
  UserId        INTEGER,
  VoteTypeId    INTEGER,
  CreationDate  DATETIME,
  BountyAmount  INTEGER
)
CHARACTER SET utf8
COLLATE utf8_general_ci
ENGINE = InnoDB;

LOAD XML LOCAL INFILE 'stackoverflow.com/stackoverflow.com-Votes' INTO TABLE votes
ROWS IDENTIFIED BY '<row>';

