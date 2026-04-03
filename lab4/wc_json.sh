#!/bin/bash

read fileName

if [[ -f $fileName ]]; then
    noChars=$(wc -m "$fileName" | awk '{print $1}')
    noWords=$(wc -w "$fileName" | awk '{print $1}')
    noLines=$(wc -l "$fileName" | awk '{print $1}')

    mostUsedChar=$(tr -dc '[:alnum:]' < "${fileName}" |
    sed -r 's/(.)/\1\n/g' |
    sort |
    uniq -c |
    sort -n |
    tail -1 |
    awk '{print $1}'
    )

    mostUsedWord=$(tr -cs '[:alnum:]' '\n' < "${fileName}" |
    tr 'A-Z' 'a-z' |
    sort |
    uniq -c |
    sort -n |
    tail -1 |
    awk '{print $1}'
    )

    echo "{
    \"file\":\"${fileName}\"
    \"noChars\":\"${noChars}\",
    \"noWords\":\"${noWords}\",
    \"noLines\":\"${noLines}\",
    \"mostUsedChar\":\"${mostUsedChar}\",
    \"mostUsedWord\":\"${mostUsedWord}\"
}"
fi
