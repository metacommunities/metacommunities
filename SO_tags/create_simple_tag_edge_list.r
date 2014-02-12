# ==============================================================================
# create a CSV listing all connections (edges) between tags with the
# 'edge list' format as shown here:
# https://gephi.org/users/supported-graph-formats/csv-format/
# note that there will be no 'weight' corresponding to the edges
# ==============================================================================

library(RMySQL)
library(data.table)
library(igraph)

wd <- "/nobackup/sharpls2/stack_exchange_data_dump_jun_2013"
edg_file <- file.path(wd, "tag_count50_edge2.csv")
gph_file <- file.path(wd, "tag_count50_edge2.graphml")

m   <- dbDriver("MySQL")
con <- dbConnect(m, user="so_import", password="fancyTea", dbname="so")    

cat("    prepping data")
# interesting tag ids
tag <- dbGetQuery(con, "SELECT id, tag FROM tag WHERE count_gte50 = 1;")
tag <- data.table(tag)
setkey(tag, id)
cat(" .")
posttag <- dbGetQuery(con, "SELECT pid, tid FROM posttag_gte50;")
cat(" .")
posttag_p <- data.table(posttag)
setkey(posttag_p, pid)
cat(" .")
posttag_t <- data.table(posttag)
setkey(posttag_t, tid)
cat(" .\n")

# add header
cat('"from","to"\n', file=edg_file)

# begin counting
for (ti in tag$id) {

  pids <- posttag_t[J(ti)]$pid
  tids <- posttag_p[J(pids)]$tid
  tids <- as.data.frame(table(tids))
  names(tids) <- c('to', 'count')
  tids$to <- as.numeric(as.character(tids$to))
  tids <- data.frame(
    from = ti,
    tids
  )
  
  # remove ids smaller than current from table
  tids <- tids[tids$to > ti, ]
  # only keep edges with a count of 2 or more
  tids <- tids[tids$count >= 2, ]
  
  if (nrow(tids) > 0) {
    # replace ids with tag names
    tids$from <- tag[J(ti)]$tag
    tids$to   <- tag[J(tids$to)]$tag

    # append to file
    write.table(tids, file=edg_file, append=TRUE, sep=",", row.names=FALSE,
      col.names=FALSE)
  }  
  
  # progress
  progress <- which(tag$id == ti) / length(tag$id) * 100
  progress <- format(round(progress, 1), width=5, nsmall=1)  
  cat("    processing: ", progress, "% complete\r", sep="")
}
cat("    processing: ", progress, "% complete\n", sep="")

# output to a graphml object
edg_lst <- read.csv(file=edg_file)
edg_lst <- graph.data.frame(edg_lst)
write.graph(edg_lst, file=gph_file, format="graphml")

