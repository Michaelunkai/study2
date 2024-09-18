def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nWhich of the following is the GREATEST security concern with respect to BYOD?\nA. The filtering of sensitive data out of data flows at geographic boundaries\nB. Removing potential bottlenecks in data transmission paths\nC. The transfer of corporate data onto mobile corporate devices\nD. The migration of data into and out of the network in an uncontrolled manner",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nThe Chief Information Security Officer (CISO) is concerned that certain systems administrators with privileged access may be reading other users' emails. Review of a tool's output shows the administrators have used web mail to log into other users' inboxes. Which of the following tools would show this type of output?\nA. Log analysis tool\nB. Password cracker\nC. Command-line tool\nD. File integrity monitoring tool",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nA power outage is caused by a severe thunderstorm and a facility is on generator power. The CISO decides to activate a plan and shut down non-critical systems to reduce power consumption. Which of the following is the CISO activating to identify critical systems and the required steps?\nA. BIA\nB. CERT\nC. IRP\nD. COOP",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nA pharmaceutical company is considering moving its technology operations from on-premises to externally-hosted to reduce costs while improving security and resiliency. These operations contain data that includes the prescription records, medical doctors' notes about treatment options, and the success rates of prescribed drugs. The company wants to maintain control over its operations because many custom applications are in use. Which of the following options represent the MOST secure technical deployment options? (Select THREE).\nA. Single tenancy\nB. Multi-tenancy\nC. Community\nD. Public\nE. Private\nF. Hybrid\nG. Saas\nH. Iaas\nI. Paas",
            "answer": "A, E, H"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nWhich of the following describes a contract that is used to define the various levels of maintenance to be provided by an external business vendor in a secure environment?\nA. NDA\nB. MOU\nC. BIA\nD. SLA",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nDuring a security assessment, activities were divided into two phases: internal and external exploitation. The security assessment team set a hard time limit on external activities before moving to a compromised box within the enterprise perimeter. Which of the following methods is the assessment team most likely to employ NEXT?\nA. Pivoting from the compromised, moving laterally through the enterprise, and trying to exfiltrate data and compromise devices\nB. Conducting a social engineering attack attempt with the goal of accessing the compromised box physically\nC. Exfiltrating network scans from the compromised box as a precursor to social media reconnaissance\nD. Open-source intelligence gathering to identify the network perimeter and scope to enable further system compromises",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nDuring the decommissioning phase of a hardware project, a security administrator is tasked with ensuring no sensitive data is released inadvertently. All paper records are scheduled to be shredded in a crosscut shredder, and the waste will be burned. The system drives and removable media have been removed prior to e-cycling the hardware. Which of the following would ensure no data is recovered from the system drives once they are disposed of?\nA. Overwriting all HDD blocks with an alternating series of data\nB. Physically disabling the HDDs by removing the drive head\nC. Demagnetizing the hard drive using a degausser\nD. Deleting the UEFI boot loaders from each HDD",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nA Chief Information Security Officer (CISO) is reviewing the controls in place to support the organization's vulnerability management program. The CISO finds patching and vulnerability scanning policies and procedures are in place. However, the CISO is concerned the organization is siloed and is not maintaining awareness of new risks to the organization. The CISO determines systems administrators need to participate in industry security events. Which of the following is the CISO looking to improve?\nA. Vendor diversification\nB. System hardening standards\nC. Bounty programs\nD. Threat awareness\nE. Vulnerability signatures",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nWhile attending a meeting with the human resources department, an organization's information security officer sees an employee using a username and password written on a memo pad to log into a specific service. When the information security officer inquires further as to why passwords are being written down, the response is that there are too many passwords to remember for all the different services the human resources department is required to use. Additionally, each password has specific complexity requirements and different expiration time frames. Which of the following would be the BEST solution for the information security officer to recommend?\nA. Utilizing MFA\nB. Implementing SSO\nC. Deploying 802.1X\nD. Pushing SAML adoption\nE. Implementing TACACS",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nA security engineer is managing operational, excess, and available equipment for a customer. Three pieces of expensive leased equipment, which are supporting a highly confidential portion of the customer network, have recently been taken out of operation. The engineer determines the equipment lease runs for another 18 months. Which of the following is the BEST course of action for the engineer to take to decommission the equipment properly?\nA. Remove any labeling indicating the equipment was used to process confidential data and mark it as available for reuse.\nB. Return the equipment to the leasing company and seek a refund for the unused time.\nC. Redeploy the equipment to a less sensitive part of the network until the lease expires.\nD. Securely wipe all device memory and store the equipment in a secure location until the end of the lease.",
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
