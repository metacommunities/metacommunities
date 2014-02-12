# ==============================================================================
# create a CSV listing all connections (edges) between tags with the
# 'mixed' format as shown here:
# https://gephi.org/users/supported-graph-formats/csv-format/
# ==============================================================================

library(RMySQL)
library(data.table)


edg_lst <- "/nobackup/sharpls2/stack_exchange_data_dump_jun_2013/tag_edge_list.csv"

if (file.exists(edg_lst)) {
  file.remove(edg_lst)
}

m   <- dbDriver("MySQL")
con <- dbConnect(m, user="so_import", password="fancyTea", dbname="so")    

cat("  prepping data")
# interesting tag ids
pid <- dbGetQuery(con, "SELECT DISTINCT pid FROM posttag_gte10;")
pid <- pid$pid
cat(" .")
posttag <- dbGetQuery(con, "SELECT pid, tid FROM posttag_gte10;")
cat(" .")
posttag <- data.table(posttag)
setkey(posttag, pid)
cat(" .\n")

# begin processing
for (pi in pid) {

  tids <- posttag[J(pi)]$tid
  tids <- paste(paste(tids, collapse=','), '\n', sep='')

  cat(tids, file=edg_lst, append=TRUE)
  
  # progress
  progress <- which(pid == pi) / length(pid) * 100
  progress <- format(round(progress, 1), width=5, nsmall=1)  
  cat("  processing: ", progress, "% complete\r", sep="")
}
cat("  processing: ", progress, "% complete\n", sep="")

