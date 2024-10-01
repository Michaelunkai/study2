def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nWhen logging in to an application, users are prompted to enter a code received from a smartphone application after entering a username and password. Which of the following security concepts does this BEST represent?\nA. Biometric authentication\nB. Least privilege\nC. Role-based access\nD. Multifactor authentication",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nWhich of the following concepts would MOST likely be used to identify individual pieces of hardware throughout their life cycle?\nA. Geofencing\nB. Smart locker\nC. Chain of custody\nD. Asset tagging",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nWhich of the following layers is the FIRST step of the bottom-to-top OSI model troubleshooting approach?\nA. Network\nB. Application\nC. Presentation\nD. Physical",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nA network technician is responding to an end user who is experiencing issues while trying to connect to 123.com. Other users, however, are able to access the website by the IP address. Which of the following is MOST likely the cause of the issue?\nA. DNS\nB. DHCP\nC. FTP\nD. HTTP",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nA new wireless network was implemented with every AP linked to the others to maintain full redundancy for network links. Which of the following BEST describes this network topology?\nA. Star\nB. Bus\nC. Mesh\nD. Ring",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nA technician is required to keep all network devices configured to the same system time. Which of the following network protocols will the technician MOST likely use?\nA. DNS\nB. STP\nC. NTP\nD. DHCP",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nA device on the network is used to link hosts from multiple subnets and on different VLANs. Which of the following does this MOST likely describe?\nA. An access point\nB. A hub\nC. A proxy server\nD. A Layer 3 switch",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nA network technician is trying to determine which hop between a client and a server is causing extreme latency. Which of the following commands will allow the technician to find this information?\nA. tracert\nB. arp\nC. tcpdump\nD. netstat",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nDuring a routine network check, a technician discovers multiple IP addresses recorded in the network logs that are not listed in the company's inventory. None of the devices have wireless network cards. Which of the following would prevent unauthorized devices from gaining access to computer resources?\nA. DHCP\nB. Geofencing\nC. SFTP\nD. Port security",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nA technician needs to connect two systems. The only available path for the cabling passes close to some equipment that emits large amounts of interference. Which of the following would be the BEST type of cable to install between the two systems?\nA. Crossover\nB. Cat 3\nC. Shielded twisted pair\nD. Plenum-rated",
            "answer": "C"
        }
    ]

    score = 0

    for qa in questions_answers:
        print(qa["question"])
        user_answer = input("Your answer (A/B/C/D): ").strip().upper()
        correct_answer = qa["answer"]

        if user_answer == correct_answer:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect. The correct answer is {correct_answer}.\n")

    print("Your final score:", score, "out of", len(questions_answers))

if __name__ == "__main__":
    main()
