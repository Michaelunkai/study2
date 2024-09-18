def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nWhich of the following is used for temporary storage of program data that is cleared when the computer is turned off?\nA. CPU\nB. SSD\nC. Hard drive\nD. System memory",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nWhich of the following methods of patching allows for vendor controlled updates, reduced user interaction, and increased security of the operating system or application?\nA. Upgrading on a periodic basis\nB. Frequent patching\nC. Automatic updates\nD. Patching scheduled daily",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nWhich of the following security threats would the use of cable locks reduce?\nA. Shoulder surfing\nB. Phishing\nC. Hardware theft\nD. Dumpster diving",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nWhich of the following is a reason why password complexity is a best practice?\nA. It makes passwords harder to crack.\nB. It encourages users to write down passwords so they are not forgotten.\nC. It forces users to develop typing skills.\nD. It discourages users from using the same password with different accounts.",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nA user receives an email containing a link. When they hover the mouse over the link, the actual URL does not match the text in the body of the email and appears to be a string of random characters. Which of the following is the BEST course of action?\nA. Forward the email to a friend to ask for advice.\nB. Reply to the sender asking for confirmation that it is safe to open.\nC. Delete the email without clicking on the link.\nD. Click the link because malware protection software is installed on the computer.",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nWhich of the following components serves as temporary storage for computer operations?\nA. System board\nB. Central processing unit\nC. Random access memory\nD. Expansion card",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nThe extension .rtf is an example of which of the following file types?\nA. Document\nB. Executable\nC. Audio\nD. Speadsheet",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nWhich of the following is a common way to prevent physical theft of a laptop or workstation?\nA. Shred any sensitive information to prior to disposal.\nB. Avoid storing passwords near the computer.\nC. Practice good awareness skills when entering passwords/PINs.\nD. Cable and lock device securely attached to a solid object.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nAfter installing a new software application, a user notices that the application launches in demo mode. Which of the following needs to be done to fully activate the software package?\nA. Enter a product or license key.\nB. Contact the vendor support.\nC. Reinstall the software application.\nD. Complete the software installation.",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nA user's laptop hard drive contains sensitive information. The user often plugs the laptop into the corporate network. A sensitive file from the laptop has been found on another user's laptop. How could the user have prevented this breach?\nA. Disable file and print sharing on the laptop.\nB. Delete unused drives from the network.\nC. Remove shared keys from the key ring.\nD. Set the read-only attribute on the files.",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 11\033[0m\nA user's government identification number, birth date, and current address are considered which of the following?\nA. IMAP\nB. HTTP\nC. PII\nD. HTTPS",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 12\033[0m\nWhich of the following is the function of a CPU?\nA. Encrypts data for remote transmission\nB. Performs data computation\nC. Supplies electricity to components\nD. Provides storage location for files",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 13\033[0m\nWhen trying to activate the operating system, a user receives a notice that the software is not genuine. Which of the following security threats has occurred?\nA. Social engineering\nB. Phishing\nC. Virus attack\nD. License theft",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 14\033[0m\nA user is configuring a SOHO wireless router. The user should change the router's default administrator password for which of the following reasons?\nA. To prevent improper data transmission encryption\nB. To prevent unauthorized configuration changes\nC. To prevent social engineering attacks\nD. To increase wireless signal strength",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 15\033[0m\nA user wants to purchase a CAD application that requires 8GB of RAM to operate. Which of the following operating system types is required?\nA. 8-bit\nB. 16-bit\nC. 32-bit\nD. 64-bit",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 16\033[0m\nSeveral users want to share a common folder with high availability. Which of the following devices is BEST to use for this requirement?\nA. Large USB flash drive connected to a PC\nB. Medium capacity SATA hard drive\nC. Network attached storage appliance\nD. Firewall with security management",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 17\033[0m\nWhich of the following is the component responsible for interconnectivity of internal system devices?\nA. System case\nB. Power supply\nC. Motherboard\nD. Expansion card",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 18\033[0m\nWhich of the following software types protects a desktop from malicious attacks?\nA. Backup\nB. Antivirus\nC. Diagnostic\nD. Screensaver",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 19\033[0m\nWhich of the following internal computer components is used to connect video, audio, and network cards?\nA. CPU\nB. Motherboard\nC. Hard drive\nD. Modem",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 20\033[0m\nWhich of the following is MOST important to ensure a computer temperature is maintained within normal limits?\nA. Maintaining constant power output\nB. Ensuring sufficient airflow\nC. Keeping the case open\nD. Turning the wireless off when not needed",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 21\033[0m\nAn employee is using a desk phone that is connected only via a network cable. Which of the following technologies is the phone using?\nA. LTE\nB. GSM\nC. VoIP\nD. CDMA",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 22\033[0m\nWhich of the following file types is used to consolidate a group of files?\nA. .rtf\nB. .m3u\nC. .avi\nD. .rar",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 23\033[0m\nWhich of the following permissions is required to run a .bat file?\nA. Delete\nB. Execute\nC. Write\nD. Modify",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 24\033[0m\nAfter installing the OS on a workstation, a technician notices that everything is displayed in large windows and the viewing area is limited. Which of the following will the technician need to adjust to resolve this issue?\nA. Color depth\nB. Orientation\nC. DPI settings\nD. Resolution",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 25\033[0m\nWhich of the following connector types can be used by both mice and keyboards? (Select TWO).\nA. Thunderbolt\nB. eSATA\nC. USB\nD. PS/2\nE. FireWire",
            "answer": ["C", "D"]
        },
        {
            "question": "\033[1mQuestion 26\033[0m\nWhich of the following will allow the easiest and fastest way to share a single file between two modern smartphones without joining the same WiFi network?\nA. Micro SD card\nB. Bluetooth\nC. USB connection\nD. Infrared",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 27\033[0m\nAn end-user has 16GB of RAM installed on a computer system. Which of the following describes why the OS only uses a maximum of 4GB of RAM?\nA. The operating system is 16-bit.\nB. The computer has corrupted RAM.\nC. The computer has a defective motherboard.\nD. The operating system is 32-bit.\nE. The computer has a virus.",
            "answer": "D"
        },
        {
            "question": "\033[1mQuestion 28\033[0m\nA technician just installed a new computer. Which of the following is the BEST way to manage the cables?\nA. Line the cables up neatly and wrap them together with cable ties.\nB. Leave the cables loose to prevent interference between wires.\nC. Nail the cables to the wall.\nD. Tuck the cables neatly underneath the carpet.",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 29\033[0m\nA user wants to run a major update on a laptop. Which of the following should be considered before running any major updates?\nA. Restore folders from back up\nB. Change administrator account password\nC. Back up important folders\nD. Print all personal documents",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 30\033[0m\nWhich of the following allows for the FASTEST printer connections?\nA. Bluetooth\nB. USB\nC. Parallel\nD. Serial",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 31\033[0m\nA user needs to establish an initial password for an email account. Which of the following is the BEST example of a complex password?\nA. 01#iWant!2686612338\nB. iWantobeaCosmonau#\nC. 01c234n56789v9876x21\nD. 012iWanttobe210",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 32\033[0m\nWhich of the following is an advantage of using a 64-bit operating system?\nA. Ability to recognize an SSD\nB. Ability to obtain an IPv6 address3\nC. Ability to utilize a larger amount of RAM\nD. Ability to add two or more hard drives",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 33\033[0m\nA user has finished browsing the Internet on a public hotel workstation. Which of the following steps should be taken to BEST secure PII?\nA. Log out of the guest account and reboot\nB. Update the browsers, extensions and plugins\nC. Run a virus scan on the workstation\nD. Clear the browser cache, cookies and history",
            "answer": "D"
        }
    ]

    score = 0

    for qa in questions_answers:
        print(qa["question"])
        user_answer = input("Your answer (Enter the letter): ").strip().upper()
        correct_answer = qa["answer"]

        if isinstance(correct_answer, list):
            if user_answer in correct_answer:
                print("Correct!\n")
                score += 1
            else:
                print(f"Incorrect. The correct answers are {', '.join(correct_answer)}.\n")
        else:
            if user_answer == correct_answer:
                print("Correct!\n")
                score += 1
            else:
                print(f"Incorrect. The correct answer is {correct_answer}.\n")

    print("Your final score:", score, "out of", len(questions_answers))

if __name__ == "__main__":
    main()

