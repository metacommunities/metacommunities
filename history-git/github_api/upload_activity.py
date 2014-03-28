def upload_wide_activity(self):
  
  self.open_con()
  
  
  """
  DROP TABLE IF EXISTS wide_activity;
  
  CREATE TABLE wide_activity AS (
      SELECT
        
      FROM commit
    UNION ALL
      SELECT
        
      FROM fork
    UNION ALL
      SELECT
        
      FROM issue
    UNION ALL
      SELECT
        
      FROM pull
  );
  
  """
  
  
  
  
  self.close_con()

