def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nJoe, a security analyst, is asked by a co-worker, 'What is this AAA thing all about in the security world? Sounds like something I can use for my car.' Which of the following terms should Joe discuss in his response to his co-worker? (Select THREE).\nA. Accounting\nB. Accountability\nC. Authorization\nD. Authentication\nE. Access\nF. Agreement",
            "answer": "ACD"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nA system administrator is configuring accounts on a newly established server. Which of the following characteristics BEST differentiates service accounts from other types of accounts?\nA. They can often be restricted in privilege.\nB. They are meant for non-person entities.\nC. They require special permissions to OS files and folders.\nD. They remain disabled in operations.\nE. They do not allow passwords to be set.",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nRecently, a company has been facing an issue with shoulder surfing. Which of the following safeguards would help with this?\nA. Screen filters\nB. Biometric authentication\nC. Smart cards\nD. Video cameras",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nThe process of presenting a user ID to a validating system is known as:\nA. authorization.\nB. authentication.\nC. identification.\nD. single sign-on.",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nAn input field that is accepting more data than has been allocated for it in memory is an attribute of:\nA. buffer overflow.\nB. memory leak.\nC. cross-site request forgery.\nD. resource exhaustion.",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 6\033[0m\nWhich of the following if used would BEST reduce the number of successful phishing attacks?\nA. Two-factor authentication\nB. Application layer firewall\nC. Mantraps\nD. User training",
            "answer": "D"
        }
    ]

    score = 0

    for qa in questions_answers:
        print(qa["question"])
        user_answer = input("Your answer (Enter the letters without spaces): ").strip().upper()
        correct_answer = qa["answer"]

        if user_answer == correct_answer:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect. The correct answer is {correct_answer}.\n")

    print("Your final score:", score, "out of", len(questions_answers))

if __name__ == "__main__":
    main()
