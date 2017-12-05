-- user
CREATE TABLE IF NOT EXISTS users (
  Id              INTEGER,
  Reputation      INTEGER,
  CreationDate    DATETIME,
  DisplayName     TINYTEXT,
  LastAccessDate  DATETIME,
  WebsiteUrl      TINYTEXT,
  Location        TINYTEXT,
  Age             INTEGER,
  AboutMe         TEXT,
  Views           INTEGER,
  UpVotes         INTEGER,
  DownVotes       INTEGER,
  EmailHash       CHAR(40),
  INDEX Id (Id),
  INDEX DisplayName (DisplayName (8))
)
CHARACTER SET utf8
COLLATE utf8_general_ci
ENGINE = InnoDB;


LOAD XML LOCAL INFILE 'stackoverflow.com/stackoverflow.com-Users' INTO TABLE users
ROWS IDENTIFIED BY '<row>';
