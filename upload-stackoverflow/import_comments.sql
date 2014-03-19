CREATE TABLE IF NOT EXISTS comments (
  Id        INTEGER,
  UserId    INTEGER,
  Name      TINYTEXT,
  Date      DATETIME
)
CHARACTER SET utf8
COLLATE utf8_general_ci
ENGINE = InnoDB;


LOAD XML LOCAL INFILE 'stackoverflow.com/stackoverflow.com-Comments' INTO TABLE comments
ROWS IDENTIFIED BY '<row>';

