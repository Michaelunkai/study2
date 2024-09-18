def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nWhich of the following qualifiers removes duplicate records from a SQL SELECT statement when included in a query?\nA. UNIQUE\nB. SINGLE\nC. DISTINCT\nD. TOP 1",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nWhich of the following ORM tools enables developers to work with a database using .NET objects?\nA. Ebean\nB. Entity Framework\nC. Eclipse\nD. Hibernate",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nWhich of the following best describes the policy/and or procedure that ensures records are kept in a database for a period of time and not deleted?\nA. Data classification policy\nB. Standard operating procedure\nC. Data retention policy\nD. Global regulation",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nSeveral users received a message from the Chief Executive Officer asking them for their bank account details. Which of the following types of attacks is taking place?\nA. Denial of service\nB. Brute-force\nC. Phishing\nD. Malware",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nA company's backup plan includes only running full backups for its small database. Which of the following frequencies would be most appropriate in this situation?\nA. Daily\nB. Monthly\nC. Weekly\nD. Quarterly",
            "answer": "A"
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
