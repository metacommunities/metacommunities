library(RMySQL)
library(ggplot2)
library(scales)
library(data.table)

adj_mat <- "tag_adjacency_matrix.csv"
edg_lst <- "tag_edge_list.csv"

m   <- dbDriver("MySQL")
con <- dbConnect(m, user="so_import", password="fancyTea", dbname="so")    

cat("prepping data")
# interesting tag ids
tag <- dbGetQuery(con, "SELECT id, tag FROM tag WHERE count >= 10;")
cat(" .")
posttag <- dbGetQuery(con, "SELECT pid, tid FROM posttag_gte10;")
cat(" .")
posttag_p <- data.table(posttag)
setkey(posttag_p, pid)
cat(" .")
posttag_t <- data.table(posttag)
setkey(posttag_t, tid)
cat(" .\n")

# add header to both files
am_header <- paste('"', c('rowtag', tag$tag), '"', sep='', collapse=',')
cat(am_header, file=adj_mat, append=TRUE)
cat('\n', file=adj_mat, append=TRUE)

edg_header <- '"from","to","count"'

# begin counting
for (ti in tag$id) {

  ## the data.table way
  pids <- posttag_t[J(ti)]$pid
  tids <- posttag_p[J(pids)]$tid
  tids <- as.data.frame(table(tids))
  names(tids) <- c("tid", "count")
  tids$tid <- as.numeric(as.character(tids$tid))

  # add non-neighbours
  non_neighbours <- tag$id[!(tag$id %in% tids$tid)]
  tids <- rbind(
    tids,
    data.frame(tid=non_neighbours, count=0)
  )
  # sort
  tids <- tids[order(tids$tid), ]
  
  # append row to file
  current_tag <- paste('"', tag$tag[tag$id == ti], '",', sep='')
  cat(current_tag, file=csv, append=TRUE)
  cat(tids$count, sep=',', file=csv, append=TRUE)
  cat('\n', file=csv, append=TRUE)
  
  # progress
  progress <- which(tag$id == ti) / length(tag$id) * 100
  progress <- format(round(progress, 1), width=5, nsmall=1)  
  cat("  process: ", progress, "% complete\r", sep="")
}
cat("  process: ", progress, "% complete\n", sep="")


