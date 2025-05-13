echo "alias s$(basename "$(pwd)" | awk '{split($0,a," "); for (i in a) printf substr(a[i],1,2)}')=\"cd $(pwd)\""
