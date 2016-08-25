#!/bin/bash
csplit $1 --prefix=section '/##/' '{*}'  > /dev/null
echo 'section word counts:'
wc -w section*
