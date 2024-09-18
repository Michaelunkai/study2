def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nWhich of the following is essential to ensure an e-commerce application can receive orders without any downtime?\nA. Availability\nB. Elasticity\nC. Hybrid\nD. Scalability",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nWhich of the following will improve availability and performance in a web application?\nA. Load balancing\nB. VPN\nC. HTTPS\nD. Single sign-on",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nWhich of the following are factors in a gap analysis when considering a CSP? (Select TWO).\nA. Technical\nB. Pilot\nC. Support\nD. Benchmarks\nE. Reporting\nF. Business",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nA cloud administrator needs to provision a database server in a public cloud provider's environment. The administrator chooses the option to pay for the database software on a monthly basis. Which of the following licensing models does this describe?\nA. Evaluation\nB. Subscription\nC. Bring your own\nD. Open-source",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nA SaaS application requires users to log in using the same password as their local network password. This is an example of:\nA. single sign-on.\nB. access control list.\nC. remote desktop protocol.\nD. multifactor authentication.",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nWhich of the following is a data management aspect of operation in a cloud environment?\nA. Object storage\nB. Self-service\nC. Locality\nD. Collaboration",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nA company identifies a risk, considers the business impact, and then decides to assume the risk. Which of the following risk response strategies is represented in this example?\nA. Avoidance\nB. Acceptance\nC. Mitigation\nD. Transference",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nDue to a breach, a cloud provider needs to locate a document that defines the appropriate actions to take. Which of the following BEST describes the process the cloud provider needs to follow?\nA. Risk register\nB. Audit\nC. Change management\nD. Incident response",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nTo comply with industry standards, an organization must hire a third-party vendor to determine if its cloud environment can be breached. Which of the following is the BEST for the organization to conduct?\nA. Application scan\nB. Integrity test\nC. Penetration test\nD. Vulnerability scan",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nWhich of the following is the networking technology that will automatically direct traffic to the host that is currently using the LEAST amount of resources?\nA. Round-robin DNS\nB. Load balancing\nC. Software-defined networking\nD. Split DNS",
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

