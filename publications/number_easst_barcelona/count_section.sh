#!/bin/bash
csplit number_barcelona_aug2016.rmd --prefix=section '/##/' '{*}'  > /dev/null
echo 'section word counts:'
wc -w section*
