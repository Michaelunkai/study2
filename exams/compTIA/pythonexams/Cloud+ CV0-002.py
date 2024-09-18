def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nObjective: Execute storage provisioning\nWhich of the following storage provisioning methods is implemented at the hardware level of a SAN and can be completed in either a soft or hard basis?\nA. LUN masking\nB. Network share creation\nC. Zoning\nD. Multipathing",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nObjective: Given a scenario, implement and use proper resource monitoring techniques\nFor which of the following protocols will an administrator configure a trap to collect system state data?\nA. SNMP\nB. FTPS\nC. IPMI\nD. SMTP",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nObjective: Implement appropriate testing techniques when deploying cloud services\nWhich of the following commands provides measurements of round-trip network latency?\nA. ping\nB. route\nC. arp\nD. nslookup",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nObjective: Explain the differences between hypervisor types\nCompared to Type II hypervisors, Type I hypervisors generally have lower:\nA. numbers of VMs per host\nB. requirements for host overhead\nC. numbers of hosts installed in datacenters\nD. costs",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nObjective: Deploy solutions to meet availability requirements\nWhich of the following methods can an Administrator use to force an array to allow data to be distributed one node at a time in a private cloud implementation?\nA. Least connections\nB. Least used\nC. Best bandwidth\nD. Round robin",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nObjective: Given a scenario, implement appropriate network configurations\nWhich of the following should an administrator use when marking VLAN traffic?\nA. Virtual Local Area Network tagging\nB. Network Address Translation\nC. Subnetting\nD. Port Address Translation",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nObjective: Install, configure, and manage virtual machines and devices\nWhich of the following will allow an administrator to quickly revert a VM back to a previous state?\nA. Metadata\nB. Snapshots\nC. Extended metadata\nD. Cloning",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nObjective: Compare and contrast cloud services\nWhich of the following is the meaning of IaaS?\nA. IT as a Service\nB. Information as a Service\nC. Infrastructure as a Service\nD. Identity as a Service",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nObjective: Compare and contrast cloud services\nWhich of the following is the meaning of Paas?\nA. Ping as a Service\nB. Process as a Service\nC. Programming as a Service\nD. Platform as a Service",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nObjective: Compare and contrast cloud services\nWhich of the following is the meaning of SaaS?\nA. Solutions as a Service\nB. Software as a Service\nC. Servers as a Service\nD. Security as a Service",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 11\033[0m\nObjective: Given a scenario, implement and use proper resource monitoring techniques\nA community name is used by:\nA. WMI\nB. SMTP\nC. SNMP\nD. SMS",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 12\033[0m\nObjective: Deploy solutions to meet availability requirements\nWhich of the following high availability solutions would a cloud service provider use when deploying Software as a Service?\nA. Virtual switches\nB. Multipathing\nC. Load balancing\nD. Clustering servers",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 13\033[0m\nObjective: Explain the differences between hypervisor types\nWhich of the following hypervisor types requires the least overhead?\nA. Type II\nB. open source\nC. Type I\nD. hosted",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 14\033[0m\nObjective: Explain common performance concepts as they relate to the host and the guest\nIn a RAID 6 environment a technician is trying to calculate how many read operations would be made. How many read operations would be required in RAID 6?\nA. One\nB. Four\nC. Two\nD. Three",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 15\033[0m\nObjective: Identify access control methods\nWhich of the following allows authentication based on something you are? (Select TWO)\nA. Passwords\nB. Access badge\nC. Retina scan\nD. Key fobs\nE. Voice recognition\nF. PIN",
            "answer": "C,E"
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

