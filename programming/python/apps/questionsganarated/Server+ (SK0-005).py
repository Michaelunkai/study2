def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nA technician is troubleshooting a server issue. Which of the following should the technician do to ensure the solution can be duplicated in the future?\nA. Verify system functionality and implement preventive measures.\nB. Document the findings, actions, and outcomes throughout the process.\nC. Determine if there is a common element or symptom.\nD. Notify the impacted users before implementing any changes.",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nWhich of the following BEST describes a security control that requires validating the user's physical characteristics?\nA. OTP\nB. Biometrics\nC. RFID\nD. Security cameras",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nUsers in an office lost access to a file server following a short power outage. The server administrator noticed the server was powered off. Which of the following should the administrator do to prevent this situation in the future?\nA. Connect the server to a KVM.\nB. Use cable management.\nC. Connect the server to a redundant network.\nD. Connect the server to a UPS.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nWhich of the following access control methodologies can be described BEST as allowing a user the least access based on the jobs the user needs to perform?\nA. Scope-based\nB. Role-based\nC. Location-based\nD. Rule-based",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nA server technician is installing a new server OS on legacy server hardware. Which of the following should the technician do FIRST to ensure the OS will work as intended?\nA. Consult the HCL to ensure everything is supported.\nB. Migrate the physical server to a virtual server.\nC. Low-level format the hard drives to ensure there is no old data remaining.\nD. Make sure the case and the fans are free from dust to ensure proper cooling.",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nA server technician is installing a new server that has four network ports. Two of the network ports have been configured for the current IP addresses of the servers. Which of the following should the technician perform to ensure security best practices?\nA. Connect the unused network ports to each other to create an unusable loop.\nB. Disable the unused network ports on the server side.\nC. Connect the unused network ports to the switch for future expansion.\nD. Insert loopback adapters into the unused network ports.",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nA systems administrator is setting up a new server that will be used as a DHCP server. The administrator installs the OS but is then unable to log on using Active Directory credentials. The administrator logs on using the local administrator account and verifies the server has the correct IP address, subnet mask, and default gateway. The administrator then gets on another server and can ping the new server. Which of the following is causing the issue?\nA. Port 443 is not open on the firewall.\nB. The server is experiencing a downstream failure.\nC. The local hosts file is blank.\nD. The server is not joined to the domain.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nA technician is trying to reach marketing.intranet.com but is unable to do so by name. The technician is able to reach it by IP address, though. Which of the following is MOST likely misconfigured?\nA. The VLAN\nB. The DNS\nC. The subnet mask\nD. The default gateway",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nWhich of the following is typical of software licensing in the cloud?\nA. Per socket\nB. Perpetual\nC. Subscription-based\nD. Site-based",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nAn administrator is unable to access a Linux host running virtual servers. Upon further investigation, the administrator views the console of the server and determines the server has crashed. Which of the following is the color of the screen?\nA. White\nB. Black\nC. Green\nD. Purple\nE. Blue",
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
