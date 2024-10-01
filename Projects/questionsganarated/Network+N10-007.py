def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nA network technician is connecting to a switch to modify the configuration. DHCP is not enabled on the management port. Which of the following does the technician need to configure to connect to the device?\nA. IP address\nB. Default gateway\nC. DNS address\nD. Loopback address",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nAn architect designs the building blueprint for a new office. The IT team has to purchase equipment and cabling. Upon inspection of the building layout, it is discovered that no designation was made for network infrastructure wiring, cabling, and services for the building. Which of the following needs to be documented in the blueprint for building connectivity?\nA. HVAC\nB. Server room\nC. MDF\nD. Mechanical room",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nA network technician has been notified that an available wireless SSID is using insecure WEP encryption and has been asked to investigate what other options are available on the existing wireless hardware. The technician has found that the WAPs support AES-CCMP. Which of the following should the technician configure?\nA. WPA2\nB. MAC filtering\nC. MD5\nD. WPS",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nA technician is called to troubleshoot a client PC that is not connecting to the network. The technician first examines the LEDs on the NIC and connection to the wall jack. Then the technician runs a loopback test on the NIC. Which of the following troubleshooting skills is the technician demonstrating?\nA. Inductive reasoning\nB. OSI model bottom-to-top\nC. Trial-and-error\nD. Divide and conquer",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nUsers within an office building report wireless connectivity is sporadic. A wireless technician troubleshooting the issue notices there are multiple WAPs visible in the same hallway within 20ft (6m) of one another. Which of the following is causing the issue?\nA. Incorrect antenna type\nB. Interference\nC. Frequency mismatch\nD. Signal reflection",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nA network technician is tasked with troubleshooting intermittent network connectivity issues within an organization. Which of the following are possible network service issues? (Select TWO).\nA. Duplicate IP address\nB. Phishing\nC. MAC filtering\nD. Exhausted DHCP scope\nE. NIC teaming\nF. Content filter",
            "answer": "A,D"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nWhich of the following components should be used to manage multiple virtual machines existing on one host?\nA. Hypervisor\nB. Virtual router\nC. Virtual switch\nD. Virtual NIC",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nWhich of the following is aimed at irreversibly damaging and disabling IoT devices?\nA. PDoS\nB. Spoofing\nC. Ransomware\nD. Logic bomb\nE. MITM",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nIn troubleshooting network performance issues on a computer, a technician finds that the CAT5e cable was run through a conduit with power lines. There is plenty of spare room in the conduit, and a cable continuity test is successful. Which of the following is the MOST likely issue?\nA. Attenuation\nB. Crosstalk\nC. Incorrect cable type\nD. EMI\nE. VLAN misconfiguration",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nOne purpose of network segmentation is to:\nA. protect sensitive data from the rest of the network.\nB. make file transfers easier for end-users.\nC. allow certain services to talk to each other without a choke point\nD. hold all hardened baseline images for deployment.",
            "answer": "A"
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
