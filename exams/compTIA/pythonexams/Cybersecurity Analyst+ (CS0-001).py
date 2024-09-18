def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nA cybersecurity analyst receives a phone call from an unknown person with the number blocked on the caller ID. After starting conversation, the caller begins to request sensitive information. Which of the following techniques is being applied?\nA. Social engineering\nB. Phishing\nC. Impersonation\nD. War dialing",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nWhich of the following is the main benefit of sharing incident details with partner organizations or external trusted parties during the incident response process?\nA. It facilitates releasing incident results, findings and resolution to the media and all appropriate government agencies\nB. It shortens the incident life cycle by allowing others to document incident details and prepare reports.\nC. It enhances the response process, as others may be able to recognize the observed behavior and provide valuable insight.\nD. It allows the security analyst to defer incident-handling activities until all parties agree on how to proceed with analysis.",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nThe security analyst determined that an email containing a malicious attachment was sent to several employees within the company, and it was not stopped by any of the email filtering devices. An incident was declared. During the investigation, it was determined that most users deleted the email, but one specific user executed the attachment. Based on the details gathered, which of the following actions should the security analyst perform NEXT?\nA. Obtain a copy of the email with the malicious attachment. Execute the file on another user's machine and observe the behavior. Document all findings.\nB. Acquire a full backup of the affected machine. Reimage the machine and then restore from the full backup.\nC. Take the affected machine off the network. Review local event logs looking for activity and processes related to unknown or unauthorized software.\nD. Take possession of the machine. Apply the latest OS updates and firmware. Discuss the problem with the user and return the machine.",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nWhich of the following tools should a cybersecurity analyst use to verify the integrity of a forensic image before and after an investigation?\nA. strings\nB. sha1sum\nC. file\nD. dd\nE. gzip",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nGiven the following logs:\n\nAug 18 11:00:57 comptia sshd[5657]: Failed password for root from 10.10.10.192 port 38980 ssh2\nAug 18 23:08:26 comptia sshd[5768]: Failed password for root from 18.70.0.160 port 38156 ssh2\nAug 18 23:08:30 comptia sshd[5770]: Failed password for admin from 18.70.0.160 port 38556 ssh2\nAug 18 23:08:34 comptia sshd[5772]: Failed password for invalid user asterisk from 18.70.0.160 port 38864 ssh2\nAug 18 23:08:38 comptia sshd[5774]: Failed password for invalid user sjobeck from 10.10.1.16 port 39157 ssh2\nAug 18 23:08:42 comptia sshd[5776]: Failed password for root from 18.70.0.160 port 39467 ssh2\n\nWhich of the following can be suspected?\nA. An unauthorized user is trying to gain access from 10.10.10.192.\nB. An authorized user is trying to gain access from 10.10.10.192.\nC. An authorized user is trying to gain access from 18.70.0.160.\nD. An unauthorized user is trying to gain access from 18.70.0.160.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nA security analyst has been asked to review permissions on accounts within Active Directory to determine if they are appropriate to the user's role. During this process, the analyst notices that a user from building maintenance is part of the Domain Admin group. Which of the following does this indicate?\nA. Cross-site scripting\nB. Session hijack\nC. Privilege escalation\nD. Rootkit",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nIn the last six months, a company is seeing an increase in credential-harvesting attacks. The latest victim was the chief executive officer (CEO). Which of the following countermeasures will render the attack ineffective?\nA. Use a complex password according to the company policy.\nB. Implement an intrusion-prevention system.\nC. Isolate the CEO's computer in a higher security zone.\nD. Implement multifactor authentication.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nAfter a security breach, it was discovered that the attacker had gained access to the network by using a brute-force attack against a service account with a password that was set to not expire, even though the account had a long, complex password. Which of the following could be used to prevent similar attacks from being successful in the future?\nA. Complex password policies\nB. Account lockout\nC. Self-service password reset portal\nD. Scheduled vulnerability scans",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nA security analyst wants to capture data flowing in and out of a network. Which of the following would MOST likely assist in achieving this goal?\nA. Taking a screenshot.\nB. Analyzing network traffic and logs.\nC. Analyzing big data metadata.\nD. Capturing system image.",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nThere are reports that hackers are using home thermostats to ping a national service provider without the provider's knowledge. Which of the following attacks is occurring from these devices?\nA. IoT\nB. DDoS\nC. MITM\nD. MIMO",
            "answer": "B"
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
