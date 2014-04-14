import csv
import subprocess
import user_prompt

def ask_upload(self):
    table = "%s.%s" % (self.conf.get('big_query', 'db'), self.conf.get('big_query', 'table'))
    question = "Should I upload activity to Big Query at '%s'?" % (table)
    ans = user_prompt.query_yes_no(question)
    
    if ans == True:
        self.upload_wide_activity()
    else:
        self.logger.info("Activity not uploaded.")

def upload_wide_activity(self):
    """
    Append rows from the following tables:
        - commit
        - pull
        - fork
        - pull
        - issue
    
    into a mega wide table called 'activity'.
    
    There are five fields that are common among all these tables, these are:
        - owner
        - repo
        - owner_repo
        - event_type
        - event_created_at
    
    This is then downloaded to the user's machine (into the tmp dir) and is
    then uploaded to bigquery. This is because there is no way to simply
    transfer data from Cloud SQL to BigQuery.
    """
    
    # create wide table of all activity
    drop_tmp = "DROP TABLE IF EXISTS activity_tmp"
    
    create_tmp = """
        CREATE TEMPORARY TABLE activity_tmp AS 
              SELECT
                    owner           AS    owner,
                    repo            AS    repo,
                    owner_repo      AS    owner_repo,
                    "commit"        AS    event_type,
                    committer_date  AS    event_created_at,
                    
                    repo            AS    commit_repo,
                    owner           AS    commit_owner,
                    owner_repo      AS    commit_owner_repo,
                    sha             AS    commit_sha,
                    author_login    AS    commit_author_login,
                    author_date     AS    commit_author_date,
                    committer_login AS    commit_committer_login,
                    committer_date  AS    commit_committer_date,
                    files_n         AS    commit_files_n,
                    stats_additions AS    commit_stats_additions,
                    stats_deletions AS    commit_stats_deletions,
                    stats_total     AS    commit_stats_total,
                    
                    NULL AS fork_parent_rid,
                    NULL AS fork_parent_owner,
                    NULL AS fork_parent_repo,
                    NULL AS fork_parent_owner_repo,
                    NULL AS fork_child_rid,
                    NULL AS fork_child_owner,
                    NULL AS fork_child_repo,
                    NULL AS fork_child_owner_repo,
                    NULL AS fork_id,
                    NULL AS fork_created_at,
                    NULL AS fork_updated_at,
                    NULL AS fork_pushed_at,
                    
                    NULL AS issue_rid,
                    NULL AS issue_repo,
                    NULL AS issue_owner,
                    NULL AS issue_owner_repo,
                    NULL AS issue_id,
                    NULL AS issue_number,
                    NULL AS issue_user_login,
                    NULL AS issue_state,
                    NULL AS issue_assignee_login,
                    NULL AS issue_created_at,
                    NULL AS issue_updated_at,
                    NULL AS issue_closed_at,
                    NULL AS issue_title,
                    NULL AS issue_pull_request,
                    NULL AS issue_comments,
                    
                    NULL AS pull_id,
                    NULL AS pull_number,
                    NULL AS pull_state,
                    NULL AS pull_title,
                    NULL AS pull_user_login,
                    NULL AS pull_created_at,
                    NULL AS pull_updated_at,
                    NULL AS pull_closed_at,
                    NULL AS pull_merged_at,
                    NULL AS pull_merge_commit_sha,
                    NULL AS pull_assignee_login,
                    NULL AS pull_commits,
                    NULL AS pull_comments,
                    NULL AS pull_head_label,
                    NULL AS pull_head_ref,
                    NULL AS pull_head_sha,
                    NULL AS pull_head_owner,
                    NULL AS pull_head_repo,
                    NULL AS pull_head_owner_repo,
                    NULL AS pull_head_fork,
                    NULL AS pull_head_created_at,
                    NULL AS pull_head_updated_at,
                    NULL AS pull_head_pushed_at,
                    NULL AS pull_base_label,
                    NULL AS pull_base_ref,
                    NULL AS pull_base_sha,
                    NULL AS pull_base_owner,
                    NULL AS pull_base_repo,
                    NULL AS pull_base_owner_repo
                FROM commit
            UNION ALL
                SELECT
                    parent_owner        AS    owner,
                    parent_repo         AS    repo,
                    parent_owner_repo   AS    owner_repo,
                    "fork"              AS    event_type,
                    created_at          AS    event_created_at,
                    
                    NULL AS commit_repo,
                    NULL AS commit_owner,
                    NULL AS commit_owner_repo,
                    NULL AS commit_sha,
                    NULL AS commit_author_login,
                    NULL AS commit_author_date,
                    NULL AS commit_committer_login,
                    NULL AS commit_committer_date,
                    NULL AS commit_files_n,
                    NULL AS commit_stats_additions,
                    NULL AS commit_stats_deletions,
                    NULL AS commit_stats_total,

                    parent_rid          AS    fork_parent_rid,
                    parent_owner        AS    fork_parent_owner,
                    parent_repo         AS    fork_parent_repo,
                    parent_owner_repo   AS    fork_parent_owner_repo,
                    child_rid           AS    fork_child_rid,
                    child_owner         AS    fork_child_owner,
                    child_repo          AS    fork_child_repo,
                    child_owner_repo    AS    fork_child_owner_repo,
                    id                  AS    fork_id,
                    created_at          AS    fork_created_at,
                    updated_at          AS    fork_updated_at,
                    pushed_at           AS    fork_pushed_at,
                    
                    NULL AS issue_rid,
                    NULL AS issue_repo,
                    NULL AS issue_owner,
                    NULL AS issue_owner_repo,
                    NULL AS issue_id,
                    NULL AS issue_number,
                    NULL AS issue_user_login,
                    NULL AS issue_state,
                    NULL AS issue_assignee_login,
                    NULL AS issue_created_at,
                    NULL AS issue_updated_at,
                    NULL AS issue_closed_at,
                    NULL AS issue_title,
                    NULL AS issue_pull_request,
                    NULL AS issue_comments,
                    
                    NULL AS pull_id,
                    NULL AS pull_number,
                    NULL AS pull_state,
                    NULL AS pull_title,
                    NULL AS pull_user_login,
                    NULL AS pull_created_at,
                    NULL AS pull_updated_at,
                    NULL AS pull_closed_at,
                    NULL AS pull_merged_at,
                    NULL AS pull_merge_commit_sha,
                    NULL AS pull_assignee_login,
                    NULL AS pull_commits,
                    NULL AS pull_comments,
                    NULL AS pull_head_label,
                    NULL AS pull_head_ref,
                    NULL AS pull_head_sha,
                    NULL AS pull_head_owner,
                    NULL AS pull_head_repo,
                    NULL AS pull_head_owner_repo,
                    NULL AS pull_head_fork,
                    NULL AS pull_head_created_at,
                    NULL AS pull_head_updated_at,
                    NULL AS pull_head_pushed_at,
                    NULL AS pull_base_label,
                    NULL AS pull_base_ref,
                    NULL AS pull_base_sha,
                    NULL AS pull_base_owner,
                    NULL AS pull_base_repo,
                    NULL AS pull_base_owner_repo
                FROM fork
            UNION ALL
                SELECT
                    repo            AS    owner,
                    owner           AS    repo,
                    owner_repo      AS    owner_repo,
                    "issue"         AS    event_type,
                    created_at      AS    event_created_at,
                    
                    NULL AS commit_repo,
                    NULL AS commit_owner,
                    NULL AS commit_owner_repo,
                    NULL AS commit_sha,
                    NULL AS commit_author_login,
                    NULL AS commit_author_date,
                    NULL AS commit_committer_login,
                    NULL AS commit_committer_date,
                    NULL AS commit_files_n,
                    NULL AS commit_stats_additions,
                    NULL AS commit_stats_deletions,
                    NULL AS commit_stats_total,
                    
                    NULL AS fork_parent_rid,
                    NULL AS fork_parent_owner,
                    NULL AS fork_parent_repo,
                    NULL AS fork_parent_owner_repo,
                    NULL AS fork_child_rid,
                    NULL AS fork_child_owner,
                    NULL AS fork_child_repo,
                    NULL AS fork_child_owner_repo,
                    NULL AS fork_id,
                    NULL AS fork_created_at,
                    NULL AS fork_updated_at,
                    NULL AS fork_pushed_at,
                    
                    rid             AS    issue_rid,
                    repo            AS    issue_repo,
                    owner           AS    issue_owner,
                    owner_repo      AS    issue_owner_repo,
                    id              AS    issue_id,
                    number          AS    issue_number,
                    user_login      AS    issue_user_login,
                    state           AS    issue_state,
                    assignee_login  AS    issue_assignee_login,
                    created_at      AS    issue_created_at,
                    updated_at      AS    issue_updated_at,
                    closed_at       AS    issue_closed_at,
                    title           AS    issue_title,
                    pull_request    AS    issue_pull_request,
                    comments        AS    issue_comments,
                    
                    NULL AS pull_id,
                    NULL AS pull_number,
                    NULL AS pull_state,
                    NULL AS pull_title,
                    NULL AS pull_user_login,
                    NULL AS pull_created_at,
                    NULL AS pull_updated_at,
                    NULL AS pull_closed_at,
                    NULL AS pull_merged_at,
                    NULL AS pull_merge_commit_sha,
                    NULL AS pull_assignee_login,
                    NULL AS pull_commits,
                    NULL AS pull_comments,
                    NULL AS pull_head_label,
                    NULL AS pull_head_ref,
                    NULL AS pull_head_sha,
                    NULL AS pull_head_owner,
                    NULL AS pull_head_repo,
                    NULL AS pull_head_owner_repo,
                    NULL AS pull_head_fork,
                    NULL AS pull_head_created_at,
                    NULL AS pull_head_updated_at,
                    NULL AS pull_head_pushed_at,
                    NULL AS pull_base_label,
                    NULL AS pull_base_ref,
                    NULL AS pull_base_sha,
                    NULL AS pull_base_owner,
                    NULL AS pull_base_repo,
                    NULL AS pull_base_owner_repo
                FROM issue
            UNION ALL
                SELECT
                    base_owner        AS    owner,
                    base_repo         AS    repo,
                    base_owner_repo   AS    owner_repo,
                    "pull"            AS    event_type,
                    created_at        AS    event_created_at,
                    
                    NULL AS commit_repo,
                    NULL AS commit_owner,
                    NULL AS commit_owner_repo,
                    NULL AS commit_sha,
                    NULL AS commit_author_login,
                    NULL AS commit_author_date,
                    NULL AS commit_committer_login,
                    NULL AS commit_committer_date,
                    NULL AS commit_files_n,
                    NULL AS commit_stats_additions,
                    NULL AS commit_stats_deletions,
                    NULL AS commit_stats_total,
                    
                    NULL AS fork_parent_rid,
                    NULL AS fork_parent_owner,
                    NULL AS fork_parent_repo,
                    NULL AS fork_parent_owner_repo,
                    NULL AS fork_child_rid,
                    NULL AS fork_child_owner,
                    NULL AS fork_child_repo,
                    NULL AS fork_child_owner_repo,
                    NULL AS fork_id,
                    NULL AS fork_created_at,
                    NULL AS fork_updated_at,
                    NULL AS fork_pushed_at,
                    
                    NULL AS issue_rid,
                    NULL AS issue_repo,
                    NULL AS issue_owner,
                    NULL AS issue_owner_repo,
                    NULL AS issue_id,
                    NULL AS issue_number,
                    NULL AS issue_user_login,
                    NULL AS issue_state,
                    NULL AS issue_assignee_login,
                    NULL AS issue_created_at,
                    NULL AS issue_updated_at,
                    NULL AS issue_closed_at,
                    NULL AS issue_title,
                    NULL AS issue_pull_request,
                    NULL AS issue_comments,

                    id                  AS    pull_id,
                    number              AS    pull_number,
                    state               AS    pull_state,
                    title               AS    pull_title,
                    user_login          AS    pull_user_login,
                    created_at          AS    pull_created_at,
                    updated_at          AS    pull_updated_at,
                    closed_at           AS    pull_closed_at,
                    merged_at           AS    pull_merged_at,
                    merge_commit_sha    AS    pull_merge_commit_sha,
                    assignee_login      AS    pull_assignee_login,
                    commits             AS    pull_commits,
                    comments            AS    pull_comments,
                    head_label          AS    pull_head_label,
                    head_ref            AS    pull_head_ref,
                    head_sha            AS    pull_head_sha,
                    head_owner          AS    pull_head_owner,
                    head_repo           AS    pull_head_repo,
                    head_owner_repo     AS    pull_head_owner_repo,
                    head_fork           AS    pull_head_fork,
                    head_created_at     AS    pull_head_created_at,
                    head_updated_at     AS    pull_head_updated_at,
                    head_pushed_at      AS    pull_head_pushed_at,
                    base_label          AS    pull_base_label,
                    base_ref            AS    pull_base_ref,
                    base_sha            AS    pull_base_sha,
                    base_owner          AS    pull_base_owner,
                    base_repo           AS    pull_base_repo,
                    base_owner_repo     AS    pull_base_owner_repo
                FROM pull
    """
    
    drop_activity = "DROP TABLE IF EXISTS activity"
    
    create_activity = "CREATE TABLE activity LIKE activity_tmp"
    
    insert_activity = """
        INSERT INTO activity
            SELECT * FROM activity_tmp ORDER BY event_created_at DESC
    """
    
    # do it
    self.logger.info("Merging contents from 'commit', 'fork', 'issue', and 'pull' tables.")
    self.open_con(fetchall=False)
    self.cur.execute(drop_tmp)
    self.cur.execute(create_tmp)
    self.cur.execute(drop_activity)
    self.cur.execute(create_activity)
    self.cur.execute(insert_activity)
    self.cur.execute(drop_tmp)
    
    # download contents table and save to CSV
    self.logger.info("Downloading 'activity' table.")
    self.cur.execute("SELECT * FROM activity")
    
    tmp_file = "/tmp/activity.csv"
    with open(tmp_file, 'w') as out:
        csv_out = csv.writer(out, quotechar='"', escapechar='\\',
                             doublequote=True, quoting=csv.QUOTE_MINIMAL,
                             lineterminator='\n')
        for row in self.cur:
            csv_out.writerow(row)
    
    # upload to BQ
    table = "%s.%s" % (self.conf.get('big_query', 'db'), self.conf.get('big_query', 'table'))
    question = "\nI'm ready to append activity to Big Query at '%s', you may want to delete this table if it already exists. You ready?" % (table)
    ans = user_prompt.query_yes_no(question)
    
    if ans == True:
        self.logger.info("Uploading to table '%s' in bigquery." % (table)) 
        
        bq_cmd = "bq load --source_format=CSV %s %s bigquery_schema/activity" % (table, tmp_file)
        process = subprocess.Popen(bq_cmd.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output
        
        self.logger.info("Done.")
    else:
        self.logger.info("Upload aborted.")
    
    self.close_con()

