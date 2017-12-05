import bq
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

client = bq.Client.Get()

query_web = "SELECT name, full_name, owner, description, fork FROM [metacommunities:github_proper.repo_list] where name contains '.io' or  name contains '.com'"
query_dot = "SELECT name, full_name, owner, description, fork FROM [metacommunities:github_proper.repo_list] where name contains 'dot' or  name contains 'dotfile'"
query_test = "SELECT name, full_name, owner, description, fork FROM [metacommunities:github_proper.repo_list] where name contains 'test'"


queries  = {'web':query_web, 'dotfile':query_dot, 
			'test':query_test}


df = pd.DataFrame()

for q in queries:
	fields, data = client.ReadSchemaAndRows(client.Query(queries[q])['configuration']['query']['destinationTable'], max_rows = 1000000)
	colnames = [f['name'] for f in fields]
	df_temp = pd.DataFrame(data, columns = colnames)
	df_temp['type'] = q
	df = df.append(df_temp)
