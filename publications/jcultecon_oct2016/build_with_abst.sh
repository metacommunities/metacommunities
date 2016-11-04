#!/bin/bash

Rscript knit.r
pandoc --filter pandoc-fignos  --latex-engine=xelatex --bibliography=ref_bibs/google_analytics.bib --bibliography=ref_bibs/mackenzie.bib --bibliography=ref_bibs/metacommunities.bib -i number_jcult_econ.md -o jcultecon_abstract.pdf

#lowriter sss.odt
