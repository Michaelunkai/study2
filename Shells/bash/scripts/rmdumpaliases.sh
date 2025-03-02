awk -F= '!seen[$1]++' <(tac ~/.bashrc) | tac > ~/.bashrc.tmp && mv ~/.bashrc.tmp ~/.bashrc
