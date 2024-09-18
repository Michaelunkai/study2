def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nA Chief Financial Officer (CFO) has been receiving email messages that have suspicious links embedded from unrecognized senders. The emails ask the recipient for identity verification. The IT department has not received reports of this happening to anyone else. Which of the following is the MOST likely explanation for this behavior?\nA. The CFO is the target of a whaling attack.\nB. The CFO is the target of identity fraud.\nC. The CFO is receiving spam that got past the mail filters.\nD. The CFO is experiencing an impersonation attack.",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nJoe, an employee, knows he is going to be fired in three days. Which of the following characterizations describes the employee?\nA. An insider threat\nB. A competitor\nC. A hacktivist\nD. A state actor",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nThe IT department receives a call one morning about users being unable to access files on the network shared drives. An IT technician investigates and determines the files became encrypted at 12:00 a.m. While the files are being recovered from backups, one of the IT supervisors realizes the day is the birthday of a technician who was fired two months prior. Which of the following describes what MOST likely occurred?\nA. The fired technician placed a logic bomb.\nB. The fired technician installed a rootkit on all the affected users' computers.\nC. The fired technician installed ransomware on the file server.\nD. The fired technician left a network worm on an old work computer.",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nAn organization has a policy in place that states the person who approves firewall controls/changes cannot be the one implementing the changes. Which of the following describes this policy?\nA. Change management\nB. Job rotation\nC. Separation of duties\nD. Least privilege",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nWhich of the following would be the BEST method to prevent the physical theft of staff laptops at an open-plan bank location with a high volume of customers each day?\nA. Guards at the door\nB. Cable locks\nC. Visitor logs\nD. Cameras",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nWhich of the following disaster recovery sites would require the MOST time to get operations back online?\nA. Colocation\nB. Cold\nC. Hot\nD. Warm",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nA security manager needed to protect a high-security datacenter, so the manager installed an access control vestibule that can detect an employee's heartbeat, weight, and badge. Which of the following did the security manager implement?\nA. A physical control\nB. A corrective control\nC. A compensating control\nD. A managerial control",
            "answer": "A"
        }
    ]

    score = 0

    for qa in questions_answers:
        print(qa["question"])
        user_answer = input("Your answer (Enter the letter): ").strip().upper()
        correct_answer = qa["answer"]

        if user_answer == correct_answer:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect. The correct answer is {correct_answer}.\n")

    print("Your final score:", score, "out of", len(questions_answers))

if __name__ == "__main__":
    main()
