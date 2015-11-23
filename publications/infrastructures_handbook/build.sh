#!/bin/sh

pandoc combinatorial_infrastructures.rmd -o combinatorial_infrastructures.odt --bibliography ref_bibs/uni.bib --bibliography ref_bibs/google_analytics.bib
pandoc combinatorial_infrastructures.rmd -o combinatorial_infrastructures.pdf --bibliography ref_bibs/uni.bib --bibliography ref_bibs/google_analytics.bib
libreoffice combinatorial_infrastructures.odt


