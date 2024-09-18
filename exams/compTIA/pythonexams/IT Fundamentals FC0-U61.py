def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nWhich of the following storage units can be used to represent 1024MB?\nA. 1GB\nB. 1KB\nC. 1TB\nD. 1PB",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nAn image displayed on a monitor is an example of:\nA. input.\nB. output.\nC. processing.\nD. storage.",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nA school has a sign posted in the computer lab that says, 'Sharing passwords with others is prohibited.' This is an example of:\nA. social networking.\nB. a security policy.\nC. file sharing.\nD. instant messaging.",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nA user buys a new desktop computer and then connects a cable that allows the computer to connect to the web. Which of the following ports would MOST likely be used?\nA. DVI\nB. HDMI\nC. Ethernet\nD. Thunderbolt\nE. Bluetooth",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nWhich of the following would BEST help to protect against unauthorized use of a mobile phone?\nA. Pop-up blocker and cookie cleaner\nB. Alternate browser and private mode\nC. PIN and screen lock\nD. Encrypted messaging and time-expiring texts",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nAnn, a user, connects a new mouse to a laptop, and the mouse works with no additional steps taken by Ann. Which of the following installation types does this BEST describe?\nA. Driver installation\nB. Plug and play\nC. Web based\nD. Manual",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 7\033[0m\nWhich of the following protocols is used for secure web browsing?\nA. SFTP\nB. HTTPS\nC. L2TP\nD. IMAP",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 8\033[0m\nWhich of the following is the MOST secure password?\nA. happybirthday12\nB. HappyDay12!\nC. H*ppyBirthDay%12\nD. HappyBirthDay123",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 9\033[0m\nWhich of the following computer components is primarily responsible for preventing overheating?\nA. Fan\nB. SSD\nC. CPU\nD. Firmware",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 10\033[0m\nWhich of the following software licensing types is MOST likely to require the renewal of terms/conditions agreements and has annual fees?\nA. One-time purchase\nB. Open source\nC. Group license\nD. Subscription",
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
