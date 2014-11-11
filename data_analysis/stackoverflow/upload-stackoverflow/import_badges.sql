-- badge
CREATE TABLE IF NOT EXISTS badges (
  Id        INTEGER,
  UserId    INTEGER,
  Name      TINYTEXT,
  Date      DATETIME,
  INDEX User (UserID),
  INDEX Name (Name (8))
)
CHARACTER SET utf8
COLLATE utf8_general_ci
ENGINE = InnoDB;


LOAD XML LOCAL INFILE 'stackoverflow.com/stackoverflow.com-Badges' INTO TABLE badges
ROWS IDENTIFIED BY '<row>';

