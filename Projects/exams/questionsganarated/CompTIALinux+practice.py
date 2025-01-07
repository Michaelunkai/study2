def main():
    print("Welcome to the Exam!")

    questions_answers = [
        {
            "question": "Which of the following ls command options will list hidden files and folders?",
            "options": ["A. ls -lh", "B. ls -la", "C. ls -lr", "D. ls -lt"],
            "answer": "B"
        },
        {
            "question": "Which of the following statements BEST describes what the command cat /proc/meminfo will display?",
            "options": ["A. Hardware-specific CPU information",
                        "B. Hardware-specific motherboard information",
                        "C. Hardware-specific RAM information",
                        "D. Hardware-specific NIC information"],
            "answer": "C"
        },
        {
            "question": "A systems administrator wants to ensure users are greeted with a warning message when they log in to deter fraudulent activity. The systems administrator should:",
            "options": ["A. enforce the use of PKI.",
                        "B. implement multifactor authentication.",
                        "C. configure disk encryption.",
                        "D. create a MOTD or banner."],
            "answer": "D"
        },
        {
            "question": "A Linux server is providing time services to several VMs. Which of the following hardening techniques will BEST reduce the risk of the time server being targeted for an attack?",
            "options": ["A. Add a warning banner.",
                        "B. Change the default port.",
                        "C. Block time services.",
                        "D. Stop time services."],
            "answer": "B"
        },
        {
            "question": "A datacenter administrator assigns a ticket to a junior Linux administrator regarding a Linux server that is presenting issues with excessive CPU consumption and causing instability in a specific application. The junior Linux administrator troubleshoots the Linux server and finds several zombie processes running on it. Which of the following commands would effectively fix the issue?",
            "options": ["A. kill -9 pid",
                        "B. kill -s SIGCHLD pid",
                        "C. kill -9 all",
                        "D. kill -9 SIG pid"],
            "answer": "B"
        },
        {
            "question": "A systems administrator wants to load custom modules. Which of the following directories is most appropriate to keep load module settings persistent?",
            "options": ["A. /etc/kernel",
                        "B. /etc/modprobe.d",
                        "C. /etc/sysconfig",
                        "D. /usr/lib/modules"],
            "answer": "B"
        },
        {
            "question": "A Linux server has been experiencing performance spikes over the course of two weeks. The administrator needs to create a report and determine the cause of the performance spikes. Which of the following commands, along with information in /var/log/messages, will help troubleshoot the issue?",
            "options": ["A. vmstat",
                        "B. sar",
                        "C. loadavarage",
                        "D. uptime"],
            "answer": "B"
        },
        {
            "question": "A Linux administrator is confirming information on a system. The administrator issues a series of commands and views the following output:\n\nsearch homebizbook.com nameserver 205.70.100.12 nameserver 205.70.100.13\n\nWhich of the following commands did the administrator issue?",
            "options": ["A. cat /etc/hosts",
                        "B. cat /etc/nsswitch.conf",
                        "C. cat /etc/resolv.conf",
                        "D. cat /etc/networks"],
            "answer": "C"
        },
        {
            "question": "A Linux administrator issues the following command with root or sudo privileges:\n\nrpm -i installpackage.rpm\n\nOnce the command is issued, the console outputs the following error message: failed dependency. The administrator confirmed in a previous step that all dependencies have already been installed. Which of the following commands should the administrator issue to bypass this error message?",
            "options": ["A. rpm -e installpackage.rpm",
                        "B. rpm -i installpackage.rpm",
                        "C. rpm -i installpackage.rpm --nodeps",
                        "D. rpm -qa installpackage.rpm"],
            "answer": "C"
        },
        {
            "question": "A Linux administrator is investigating an unscheduled restart of an application server and wants to check for successful logins prior to the restart. Which of the following commands would display this information?",
            "options": ["A. who",
                        "B. last",
                        "C. dmesg",
                        "D. reboot",
                        "E. uptime"],
            "answer": "B"
        }
    ]

    for index, question_data in enumerate(questions_answers, start=1):
        question = question_data["question"]
        options = question_data["options"]
        answer = question_data["answer"]

        print(f"\nQuestion {index}: {question}")
        for option in options:
            print(option)

        user_choice = input("Your choice (A/B/C/D): ").upper()

        if user_choice == answer:
            print("Correct!")
        else:
            print(f"Wrong! The correct answer is: {answer}")

        proceed = input("Do you want to continue? (y/n): ").lower()
        if proceed != 'y':
            break

    print("Thank you for taking the Exam!")

if __name__ == "__main__":
    main()
