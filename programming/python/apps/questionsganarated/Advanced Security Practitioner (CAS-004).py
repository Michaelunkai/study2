def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nMany of an organization's recent security incidents on the corporate network involve third-party software vulnerabilities. Which of the following would reduce the risk presented by these vulnerabilities?\nA. Only allow approved applications to be installed on workstations.\nB. Block all malicious and hard to manage applications from being installed.\nC. Perform software composition analysis for all software developed in-house.\nD. Properly manage third-party libraries in the development environment.",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nA company recently migrated from on-premises to cloud to meet a new requirement that the cloud provider reacts to any security vulnerabilities related to the underlying service. Which of the following risk handling techniques is described?\nA. Transfer\nB. Avoid\nC. Accept\nD. Mitigate",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nA satellite communications ISP frequently experiences outages and degraded modes of operation over one of its legacy satellite links due to the use of deprecated hardware and software. Three days per week, on average, a contracted company must follow a checklist of 16 different high-latency commands that must be run in serial to restore nominal performance. The ISP wants this process to be automated. Which of the following techniques would be BEST suited for this requirement?\nA. Deploy SOAR utilities and runbooks.\nB. Replace the associated hardware.\nC. Provide the contractors with direct access to satellite telemetry data.\nD. Reduce link latency on the affected ground and satellite segments.",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nA security engineer estimates the company's popular web application experiences 100 attempted breaches per day. In the past four years, the company's data has been breached two times. Which of the following should the engineer report as the ARO for successful breaches?\nA. 0.5\nB. 8\nC. 50\nD. 36,500",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nAs part of its risk strategy, a company is considering buying insurance for cybersecurity incidents. Which of the following BEST describes this kind of risk response?\nA. Risk rejection\nB. Risk mitigation\nC. Risk transference\nD. Risk avoidance",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nAn organization recently started processing, transmitting, and storing its customers' credit card information. Within a week of doing so, the organization suffered a massive breach that resulted in the exposure of the customers' information. Which of the following provides the BEST guidance for protecting such information while it is at rest and in transit?\nA. NIST\nB. GDPR\nC. PCI DSS\nD. ISO",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nAn IT administrator is reviewing all the servers in an organization and notices that a server is missing crucial patches against a recent exploit that could gain root access. Which of the following describes the administrator's discovery?\nA. A vulnerability\nB. A threat\nC. A breach\nD. A risk",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nA review of the past year's attack patterns shows that attackers stopped reconnaissance after finding a susceptible system to compromise. The company would like to find a way to use this information to protect the environment while still gaining valuable attack information. Which of the following would be BEST for the company to implement?\nA. A WAF\nB. An IDS\nC. A SIEM\nD. A honeypot",
            "answer": "D"
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
