#!/bin/ 

declare -A questions
declare -A options
declare -A hints
declare -A answers
declare -A user_answers

questions[1]="What command is used to check disk space usage?"
options[1]="a) df -h\nb) du -sh\nc) lsblk"
hints[1]="Hint: The command is commonly used to report file system disk space usage."
answers[1]="a"

questions[2]="Which command is used to display the current network configuration?"
options[2]="a) ifconfig\nb) ipconfig\nc) netstat"
hints[2]="Hint: It's deprecated but still widely used."
answers[2]="a"

questions[3]="How do you list all running processes?"
options[3]="a) ps aux\nb) top\nc) htop"
hints[3]="Hint: It's the most comprehensive command for listing processes."
answers[3]="a"

questions[4]="Which command is used to search for a specific pattern in files?"
options[4]="a) find\nb) grep\nc) locate"
hints[4]="Hint: It's a powerful utility for searching text."
answers[4]="b"

questions[5]="What command is used to view the last few lines of a file?"
options[5]="a) tail -n\nb) head -n\nc) cat"
hints[5]="Hint: It outputs the end of a file."
answers[5]="a"

questions[6]="How do you install a package using apt?"
options[6]="a) apt-get install <package>\nb) apt-add-repository <package>\nc) dpkg -i <package>"
hints[6]="Hint: It's the most common package manager for Debian-based systems."
answers[6]="a"

questions[7]="Which command shows the system's current date and time?"
options[7]="a) date\nb) time\nc) cal"
hints[7]="Hint: It's a simple command that outputs the current date."
answers[7]="a"

questions[8]="How do you change the ownership of a file?"
options[8]="a) chown user:group <file>\nb) chmod 755 <file>\nc) chgrp <file>"
hints[8]="Hint: It's used to change the user and group ownership."
answers[8]="a"

questions[9]="What command is used to update the package list on a Debian-based system?"
options[9]="a) apt-get update\nb) yum update\nc) pacman -Sy"
hints[9]="Hint: It's the first step before upgrading packages."
answers[9]="a"

questions[10]="Which command is used to display the manual page of a command?"
options[10]="a) help <command>\nb) info <command>\nc) man <command>"
hints[10]="Hint: It's the primary tool for accessing documentation."
answers[10]="c"

function display_question() {
    local qnum=$1
    echo "Question $qnum: ${questions[$qnum]}"
    echo -e "${options[$qnum]}"
    echo -e "a) View Hint\nb) View Answer"
}

function display_hint() {
    local qnum=$1
    echo -e "${hints[$qnum]}"
}

function display_answer() {
    local qnum=$1
    echo "Correct answer: ${answers[$qnum]}"
}

function get_user_input() {
    local qnum=$1
    read -p "Your answer (a/b/c/hint/answer): " choice
    case $choice in
        hint)
            display_hint $qnum
            get_user_input $qnum
            ;;
        answer)
            display_answer $qnum
            get_user_input $qnum
            ;;
        a|b|c)
            user_answers[$qnum]=$choice
            ;;
        *)
            echo "Invalid choice. Please enter a, b, c, hint, or answer."
            get_user_input $qnum
            ;;
    esac
}

function calculate_score() {
    local score=0
    for i in {1..10}; do
        if [[ ${user_answers[$i]} == ${answers[$i]} ]]; then
            score=$((score + 10))
        fi
    done
    echo "Your score: $score/100"
}

function main() {
    for i in {1..10}; do
        display_question $i
        get_user_input $i
    done
    echo "Finish & Test"
    calculate_score
}

main
