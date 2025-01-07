def main():
    print("Welcome to the Exam!")

    questions_answers = [
        {
            "question": "A technician needs to replace a failed power supply on a server. The server in question only has one power supply. The server contains two processors that need 100w, five hard drives that need 9w, and a GPU that uses 200w. Which of the following power supplies should the technician use?",
            "options": ["A. 375w", "B. 425w", "C. 325w", "D. 500w"],
            "answer": "D"
        },
        {
            "question": "An organization uses a cloud storage service to store company files. The file synchronization client for this cloud service is installed on every user's computer. One user reports that a file synced with the client to their computer does not contain information a co-worker of theirs added earlier today. Indicate the BEST action to take when troubleshooting this problem.",
            "options": ["A. Exit the cloud service's client that is locally installed, restart the computer, and check to see if the file contains the information that is missing.",
                        "B. Visit the cloud service's website, locate the service status page, and determine if their is a service outage impacting the organization.",
                        "C. Open the cloud service's client that is locally installed, determine if there are any reported errors, and follow the steps provided to correct the synchronization errors.",
                        "D. Open the cloud service's client that is locally installed and check to see if there are any updates available for the client."],
            "answer": "C"
        },
        {
            "question": "A technician is helping a user configure a new mobile phone. The user could pay for purchases with the previous phone by touching the phone to the payment system. Which of the following features should the technician enable so that the user can use the new phone to also pay for purchases this way?",
            "options": ["A. PAN", "B. RFID", "C. NFC", "D. Bluetooth"],
            "answer": "C"
        },
        {
            "question": "A user recently reported that every few days the system clock is approximately three minutes behind. The user also received an error message on the BIOS screen. Which of the following would MOST likely fix the clock issue?",
            "options": ["A. Enable dual-channel memory by adding a second RAM stick.",
                        "B. Install a new power supply.",
                        "C. Replace the motherboard's CMOS battery.",
                        "D. Configure the PC to be an NTP server."],
            "answer": "C"
        },
        {
            "question": "A user with a new 5G smartphone notices the device has separated at the seam on one edge and is measurably thicker at that point. Which of the following actions should the user take FIRST?",
            "options": ["A. Power off the smartphone and place it in a bucket of rice for 48 hours.",
                        "B. Place the smartphone in a refrigerator between 35°F (1.6°C) and 40°F ( 4.4°C) overnight.",
                        "C. Fully deplete the phone's battery and then charge it to 100%.",
                        "D. Contact the smartphone manufacturer for warranty support."],
            "answer": "D"
        },
        {
            "question": "A technician is replacing a laptop's HDD with an SSD. Which of the following should the technician do FIRST?",
            "options": ["A. Create a backup of the HDD.",
                        "B. Upgrade the RAM on the laptop.",
                        "C. Enable SSD support at BIOS.",
                        "D. Install SSD drivers inside the OS."],
            "answer": "A"
        },
        {
            "question": "Which of the following technologies has the FASTEST connection speed?",
            "options": ["A. Fiber", "B. Satellite", "C. DSL", "D. Cable"],
            "answer": "A"
        },
        {
            "question": "A PC in a conference room will be connected to a large-screen TV for video presentations during training sessions. Which of the following video connectors is the MOST likely choice for this environment?",
            "options": ["A. Video Graphics Array", "B. Thunderbolt", "C. Digital Visual Interface", "D. High-Definition Multimedia Interface"],
            "answer": "D"
        }
    ]

    for index, question_data in enumerate(questions_answers, start=1):
        question = question_data["question"]
        options = question_data["options"]
        answer = question_data["answer"]

        print(f"\nQuestion {index}: {question}")
        for option in options:
            print(option)

        user_choice = input("Your choice (A/B/C/D): ").upper()

        if user_choice == answer:
            print("Correct!")
        else:
            print(f"Wrong! The correct answer is: {answer}")

        proceed = input("Do you want to continue? (yes/no): ").lower()
        if proceed != 'yes':
            break

    print("Thank you for taking the Exam!")

if __name__ == "__main__":
    main()
