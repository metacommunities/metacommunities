# ==============================================================================
# mini-dashboards for each of the "interesting" regions on the log-log
# power law graph
# ==============================================================================

load("ptdata.RData")

library(ggplot2)
library(grid)

# First region contains lots of repos which all have a short lifespan
# and, subsequently, a very small amount of activity. Though the actual
# lifespan varies considerably for each repo. In terms of typology, they
# mainly consist of 'Isolated Forks' and 'PR Issuer'. The plan is to get
# this all on to some kind of mini-dashboard.

sdat <- dat1
p.file <- "sp1-type.png"

type <- table(sdat$type)
type <- as.data.frame(type)
names(type) <- c("type", "freq")
# rate per 10,000
type$rate <- type$freq / sum(type$freq) * 10000

p.type <-
  ggplot(type, aes(x=rate, y=type)) +
    geom_errorbarh(aes(xmin=0, xmax=rate), height=0, size=5) +
    theme_bw(base_size=10) +
    labs(x="Count per 10,000", y="")

ggsave(p.type, filename=p.file, width=4, height=2.5)
