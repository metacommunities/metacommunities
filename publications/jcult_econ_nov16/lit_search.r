library(scilitlearn)
library(dplyr)
library(ggplot2)
wos = load_data('data/jcultecon_all.tsv')
r = search_term(wos, 'facebook', format_as_bibtex = FALSE)
r$AF
ls(pos='package:scilitlearn')
cited_references_time(wos)
r2 = search_term(wos, 'perform', format_as_bibtex = FALSE)
r2b = search_term(wos, 'perform', format_as_bibtex = T )
r2b
r2$TI 
r2 %>%  select(AU,TI) %>% View
