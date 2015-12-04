pandoc -f markdown+pipe_tables --template /home/mackenza/template.latex --bibliography /home/mackenza/Documents/ref_bibs/mackenzie.bib --bibliography "/home/mackenza/Documents/ref_bibs/data_forms_thought.bib" --bibliography "/home/mackenza/Documents/ref_bibs/google_analytics.bib" --bibliography "/home/mackenza/Documents/ref_bibs/R.bib" --bibliography "/home/mackenza/Documents/ref_bibs/machine_learning.bib" -o "mackenzie_code_city.pdf" "mackenzie_code_city.md" --latex-engine=xelatex
evince mackenzie_code_city.pdf

