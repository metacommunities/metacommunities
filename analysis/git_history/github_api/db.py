import MySQLdb
import MySQLdb.cursors

def open_con(self, fetchall=True):
    """
    Open connection to mysql db.
    """
    
    if fetchall == True:
        self.con = MySQLdb.connect(host=self.conf.get('mysql', 'host'),
                                   user=self.conf.get('mysql', 'user'),
                                   passwd=self.conf.get('mysql', 'passwd'),
                                   db=self.conf.get('mysql', 'db'),
                                   charset='utf8',
                                   use_unicode=False)
    else:
        self.con = MySQLdb.connect(host=self.conf.get('mysql', 'host'),
                                   user=self.conf.get('mysql', 'user'),
                                   passwd=self.conf.get('mysql', 'passwd'),
                                   db=self.conf.get('mysql', 'db'),
                                   charset='utf8',
                                   cursorclass = MySQLdb.cursors.SSCursor,
                                   use_unicode=False)
    
    self.cur = self.con.cursor()


def close_con(self):
    """
    Commit inserts and close db connection.
    """
    
    self.cur.close()
    self.con.commit()
    self.con.close()


def create_db(self, drop_db):
    """
    Maybe drop the database. Create database and tables in the db specific in
    the config, if any don't exists.
    """
    
    self.logger.info("Checking '%s' database..." % (self.conf.get('mysql', 'db')))
    
    con = MySQLdb.connect(host=self.conf.get('mysql', 'host'),
                          user=self.conf.get('mysql', 'user'),
                          passwd=self.conf.get('mysql', 'passwd'))
    cur = con.cursor()
    
    # wipe those tables
    if drop_db:
        drop_sql = "DROP DATABASE IF EXISTS %s;" % (self.conf.get('mysql', 'db'))
        cur.execute(drop_sql)
        self.logger.info("Dropped database %s" % (self.conf.get('mysql', 'db')))
    
    # create db
    create_sql = "CREATE DATABASE IF NOT EXISTS %s" % (self.conf.get('mysql', 'db'))
    cur.execute(create_sql)
    
    # use db
    use_sql = "USE %s;" % (self.conf.get('mysql', 'db'))
    cur.execute(use_sql)
    
    # create tables
    repo_list_sql = """
        CREATE TABLE IF NOT EXISTS repo_list (
            id                  INTEGER AUTO_INCREMENT PRIMARY KEY,
            name                TINYTEXT,
            full_name           TINYTEXT,
            owner               TINYTEXT,
            description         TEXT,
            fork                TINYINT(1) NOT NULL DEFAULT 0
        )
    """
    cur.execute(repo_list_sql)
    
    repo_sql = """
        CREATE TABLE IF NOT EXISTS repo_summary (
            id                      INTEGER AUTO_INCREMENT PRIMARY KEY,
            name                    TINYTEXT,
            full_name               TINYTEXT,
            owner                   TINYTEXT,
            created_at              DATETIME,
            description             TEXT,
            is_fork                 TINYINT(1),
            commits                 MEDIUMINT NOT NULL DEFAULT 0,
            forks                   MEDIUMINT NOT NULL DEFAULT 0,
            issues                  MEDIUMINT NOT NULL DEFAULT 0,
            pull_requests           MEDIUMINT NOT NULL DEFAULT 0,
            pushed_at               DATETIME NULL,
            language                TINYTEXT,
            last_commit             DATETIME NULL,
            last_fork               DATETIME NULL,
            last_pull_request       DATETIME NULL,
            collaborators           MEDIUMINT NOT NULL DEFAULT 0,
            contributors            MEDIUMINT NOT NULL DEFAULT 0,
            last_summary_updated    DATETIME NOT NULL,
            backlog_complete        TINYINT(1) NOT NULL DEFAULT 0
        )
    """
    cur.execute(repo_sql)
    
    commit_sql = """
        CREATE TABLE IF NOT EXISTS commit (
            rid                 INTEGER,
            repo                TINYTEXT,
            owner               TINYTEXT,
            owner_repo          TINYTEXT,
            sha                 CHAR(40) NULL,
            author_login        TINYTEXT NULL,
            author_date         DATETIME NULL,
            committer_login     TINYTEXT NULL,
            committer_date      DATETIME NULL,
            files_n             SMALLINT NULL,
            stats_additions     INTEGER NULL,
            stats_deletions     INTEGER NULL,
            stats_total         INTEGER NULL
        )
    """
    cur.execute(commit_sql)
    
    fork_sql = """
        CREATE TABLE IF NOT EXISTS fork (
            parent_rid          INTEGER,
            parent_owner        TINYTEXT,
            parent_repo         TINYTEXT,
            parent_owner_repo   TINYTEXT,
            child_rid           INTEGER,
            child_owner         TINYTEXT,
            child_repo          TINYTEXT,
            child_owner_repo    TINYTEXT,
            id                  INTEGER NULL,
            created_at          DATETIME NULL,
            updated_at          DATETIME NULL,
            pushed_at           DATETIME NULL
        )
    """
    cur.execute(fork_sql)
    
    issue_sql = """
        CREATE TABLE IF NOT EXISTS issue (
            rid                 INTEGER,
            repo                TINYTEXT,
            owner               TINYTEXT,
            owner_repo          TINYTEXT,
            id                  INTEGER,
            number              INTEGER,
            user_login          TINYTEXT,
            state               TINYTEXT,
            assignee_login      TINYTEXT,
            created_at          DATETIME,
            updated_at          DATETIME,
            closed_at           DATETIME,
            duration_s          INTEGER,
            title               TEXT,
            body                MEDIUMTEXT,
            pull_request        TINYINT(1),
            comments            SMALLINT
        )
    """
    cur.execute(issue_sql)
    
    pull_sql = """
        CREATE TABLE IF NOT EXISTS pull (
            id                    INTEGER,
            number                INTEGER,
            state                 TINYTEXT,
            title                 TEXT,
            user_login            TINYTEXT,
            body                  TEXT,
            created_at            DATETIME,
            updated_at            DATETIME,
            closed_at             DATETIME,
            merged_at             DATETIME,
            merge_commit_sha      CHAR(40),
            assignee_login        TINYTEXT,
            commits               TINYINT,
            comments              TINYINT,
            duration_s            INTEGER,
            head_label            TINYTEXT,
            head_ref              TINYTEXT,
            head_sha              CHAR(40),
            head_owner            TINYTEXT,
            head_repo             TINYTEXT,
            head_owner_repo       TINYTEXT,
            head_fork             TINYINT(1),
            head_created_at       DATETIME,
            head_updated_at       DATETIME,
            head_pushed_at        DATETIME,
            base_label            TINYTEXT,
            base_ref              TINYTEXT,
            base_sha              CHAR(40),
            base_owner            TINYTEXT,
            base_repo             TINYTEXT,
            base_owner_repo       TINYTEXT
        )
    """
    cur.execute(pull_sql)
    
    language_sql = """
        CREATE TABLE IF NOT EXISTS language (
            rid           INTEGER NOT NULL,
            name          TINYTEXT NOT NULL,
            bytes         INTEGER NOT NULL,
            last_checked  DATETIME
        )
    """
    cur.execute(language_sql)
    
    con.commit()
    cur.close()
    con.close()
    self.logger.info("Done.")


def insert(self, dat, table):
    """
    Generate an INSERT statement off of the keys of the dat dict. Determine
    if records are commited to the db.
    """
    
    fields = ', '.join(dat.viewkeys())
    values = ')s, %('.join(dat.viewkeys())
    insert_sql = "INSERT INTO " + table + " (" + fields + ") VALUES (%(" + values + ")s)"
    
    self.cur.execute(insert_sql, dat)
    
    # shall we commit to the db? -- Oh the irony...
    if self.n >= 1000:
        self.con.commit()
        #self.logger.info("        added %s records to '%s' table..." % (format(self.n, ",d"), table))
        self.n = 0
    self.n += 1
    self.N += 1
