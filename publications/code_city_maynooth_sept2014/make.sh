pandoc --bibliography "/home/mackenza/Documents/ref_bibs/data_forms_thought.bib" --bibliography "/home/mackenza/Documents/ref_bibs/google_analytics.bib" --bibliography "/home/mackenza/Documents/ref_bibs/R.bib" --bibliography "/home/mackenza/Documents/ref_bibs/machine_learning.bib" -o "mackenze_code_city.pdf" "mackenze_code_city.md" --latex-engine=xelatex
evince mackenze_code_city.pdf

