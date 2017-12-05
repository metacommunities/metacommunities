# quick way to query bigquery
import bq
client = bq.Client.Get()

query = "select * from metacommunities:github_proper.org_ultimate"
fields, data = client.ReadSchemaAndRows(client.Query(query)['configuration']['query']['destinationTable'], max_rows = 100000)
colnames = [f['name'] for f in fields]
pd.DataFrame(data, columns = fields)