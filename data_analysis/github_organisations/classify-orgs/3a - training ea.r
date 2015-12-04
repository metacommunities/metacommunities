# ==============================================================================
# initial exploratory analysis of the training data
# ==============================================================================

library(reshape)
library(ggplot2)

source("2 - load.r")

# ------------------------------------------------------------------------------
# frequency of tags
# ------------------------------------------------------------------------------

tag <- melt(org_train, id="repository_organization",
  measure=c("is_software", "is_technical", "is_education", "is_business",
    "is_games", "is_social"))

tag <- tag[tag$value != 0, ]

p.tag <-
  ggplot(tag, aes(x=variable)) +
    geom_bar()

ggsave(p.tag, file="img/p_tag_freq.png")


# ------------------------------------------------------------------------------
# dist of how many tags an org has
# ------------------------------------------------------------------------------

table(rowSums(org_train[, grep("^is_", names(org_train))]))


# ------------------------------------------------------------------------------
# frequency of org types
# ------------------------------------------------------------------------------

p.type <-
  ggplot(org_train, aes(x=factor(type))) +
    geom_bar()

ggsave(p.type, file="img/p_type_freq.png")

