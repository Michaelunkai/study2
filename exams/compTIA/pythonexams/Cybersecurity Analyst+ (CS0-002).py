def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nThe security team at a large corporation is helping the payment-processing team to prepare for a regulatory compliance audit and meet the following objectives:\n\nReduce the number of potential findings by the auditors.\nLimit the scope of the audit to only devices used by the payment-processing team for activities directly impacted by the regulations.\nPrevent the external-facing web infrastructure used by other teams from coming into scope.\nLimit the amount of exposure the company will face if the systems used by the payment-processing team are compromised.\n\nWhich of the following would be the MOST effective way for the security team to meet these objectives?\nA. Limit the permissions to prevent other employees from accessing data owned by the business unit.\nB. Segment the servers and systems used by the business unit from the rest of the network.\nC. Deploy patches to all servers and workstations across the entire organization.\nD. Implement full-disk encryption on the laptops used by employees of the payment-processing team.",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nData spillage occurred when an employee accidentally emailed a sensitive file to an external recipient. Which of the following controls would have MOST likely prevented this incident?\nA. SSO\nB. DLP\nC. WAF\nD. VDI",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nWhich of the following assessment methods should be used to analyze how specialized software performs during heavy loads?\nA. Stress test\nB. API compatibility test\nC. Code review\nD. User acceptance test\nE. Input validation",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nA large amount of confidential data was leaked during a recent security breach. As part of a forensic investigation, the security team needs to identify the various types of traffic that were captured between two compromised devices. Which of the following should be used to identify the traffic?\nA. Carving\nB. Disk imaging\nC. Packet analysis\nD. Memory dump\nE. Hashing",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nA user reports the system is behaving oddly following the installation of an approved third-party software application. The application executable was sourced from an internal repository. Which of the following will ensure the application is valid?\nA. Ask the user to refresh the existing definition file for the antivirus software.\nB. Perform a malware scan on the file in the internal repository.\nC. Hash the application's installation file and compare it to the hash provided by the vendor.\nD. Remove the user's system from the network to avoid collateral contamination.",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nA company's senior human resources administrator left for another position, and the assistant administrator was promoted into the senior position. On the official start day, the new senior administrator planned to ask for extended access permissions but noticed the permissions were automatically granted on that day. Which of the following describes the access management policy in place at the company?\nA. Mandatory-based\nB. Host-based\nC. Federated access\nD. Role-based",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nWhile reviewing incident reports from the previous night, a security analyst notices the corporate websites were defaced with political propaganda. Which of the following BEST describes this type of actor?\nA. Hacktivist\nB. Nation-state\nC. Insider threat\nD. Organized crime",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nA proposed network architecture requires systems to be separated from each other logically based on defined risk levels. Which of the following explains the reason why an architect would set up the network this way?\nA. To complicate the network and frustrate a potential malicious attacker\nB. To create a design that simplifies the supporting network\nC. To reduce the attack surface of those systems by segmenting the network based on risk\nD. To reduce the number of IP addresses that are used on the network",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nDuring a review of a potential security incident, more records than normal in a database were deleted on the first day of the month. A conversation with the database owner revealed that the deletion was expected since the records were older than seven years. Which of the following policies would have required this event to be performed?\nA. Risk assessment\nB. Data retention\nC. Access control\nD. Data loss prevention",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nA security analyst wants to deploy a system on the public Internet to collect the newest exploits that are being seen in the wild. Which of the following would BEST achieve this goal?\nA. Honeypot server\nB. Unpatched MySQL server\nC. Cloud access security broker\nD. Kubernetes management server",
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
