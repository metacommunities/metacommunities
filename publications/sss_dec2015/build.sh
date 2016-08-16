#!/bin/bash

Rscript knit.r
pandoc --filter pandoc-fignos  --latex-engine=xelatex --bibliography=ref_bibs/google_analytics.bib --bibliography=ref_bibs/mackenzie.bib --bibliography=ref_bibs/metacommunities.bib --csl=sage-harvard.csl -i sss.md -o sss.odt

lowriter sss.odt
