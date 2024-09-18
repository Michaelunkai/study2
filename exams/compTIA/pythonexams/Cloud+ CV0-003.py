def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nCompany policy dictates all systems and data must remain under the company's control. Which of the following should the systems administrator choose to migrate the current systems to the cloud?\nA. Cloud within a cloud\nB. Public cloud\nC. Community cloud\nD. Private cloud",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nA company has deployed a new cloud solution and is required to meet security compliance. Which of the following will MOST likely be executed in the cloud solution to meet security requirements?\nA. Performance testing\nB. Regression testing\nC. Vulnerability testing\nD. Usability testing",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nWhich of the following will mitigate the risk of users who have access to an instance modifying the system configurations?\nA. Implement whole-disk encryption.\nB. Deploy the latest OS patches.\nC. Deploy an anti-malware solution.\nD. Implement mandatory access control.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nA cloud administrator is working in a public cloud environment and needs to deploy database servers that require fast read/write speeds. During the deployment process, the administrator is asked which type of storage to deploy. Which of the following should the administrator select?\nA. Spinning disks\nB. Long-term\nC. SSD\nD. Hybrid",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nAn organization has an application that experiences high-usage activities during the summer, and customers often report slow response times. Which of the following actions should a cloud administrator take to correct this performance issue?\nA. Implement redundancy.\nB. Reboot the server.\nC. Raise the ticket with the service provider.\nD. Configure auto-scaling.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nA cloud administrator has built a new private cloud environment and needs to monitor all compute, storage, and network components of the environment. Which of the following protocols would be MOST useful for this task?\nA. SMTP\nB. SCP\nC. SNMP\nD. SFTP",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nAn administrator is performing an in-place upgrade on a guest VM operating system. Which of the following can be performed as a quick method to roll back to an earlier state, if necessary?\nA. A configuration file backup\nB. A full backup of the database\nC. A differential backup\nD. A VM-level snapshot",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nA cloud administrator is asked to verify a new cloud application is working as expected. Some users are reporting login issues. Which of the following testing techniques would BEST fit this exercise?\nA. Regression testing\nB. Functionality testing\nC. Usability testing\nD. Performance testing",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nA systems administrator is tasked with analyzing resource utilization metrics. Which of the following units represents the metric named StatusCheckFailed?\nA. Percent\nB. Bytes\nC. Seconds\nD. Count",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nAn organization has the following requirements that need to be met when implementing cloud services:\n\nSSO to cloud infrastructure\nOn-premises directory service\nRBAC for IT staff\n\nWhich of the following cloud models would meet these requirements?\nA. Public\nB. Community\nC. Hybrid\nD. Multitenant",
            "answer": "C"
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

