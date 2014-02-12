# ==============================================================================
# explore tag frequency
# ==============================================================================

library(RMySQL)
library(ggplot2)
library(scales)

m   <- dbDriver("MySQL")
con <- dbConnect(m, user="so_import", password="fancyTea", dbname="so")    


# which are the frequent tags?
count_tags = "
  SELECT pt.tid, t.tag, count(*) AS count
  FROM posttag AS pt, tag AS t
  WHERE t.id = pt.tid
  GROUP BY pt.tid
  ORDER BY count DESC;
"

res <- dbGetQuery(con, count_tags)

tag.levels <- res$tag[order(res$count, decreasing=FALSE)]
res$tag <- factor(res$tag, levels=tag.levels)

# top 100 tags
p.tag.count <-
  ggplot(res[1:100, ], aes(x=factor(tag), y=count)) +
    geom_bar(stat="identity") +
    xlab("") +
    scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
                   labels = trans_format("log10", math_format(10^.x))) +
    coord_flip()

# how many tags are used 10 or more times?
sum(res$count >  10) # 24,120
sum(res$count >  50) # 12,206
sum(res$count > 100) #  8,339

# frequency of counts...
p.frequency <-
  ggplot(res, aes(x=count)) +
    geom_histogram(binwidth=100) +
    xlim(0, 10^5)

