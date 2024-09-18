def main():
    questions_answers = [
        {
            "question": "\033[1mQuestion 1\033[0m\nQ3 2020 has just ended, and now a data analyst needs to create an ad-hoc sales report that demonstrates how well the Q3 2020 promotion went versus last year's Q3 promotion. Which of the following date parameters should the analyst use?\nA. 2019 vs. YTD 2020\nB. Q3 2019 vs. Q3 2020\nC. YTD 2019 vs. YTD 2020\nD. Q4 2019 vs. Q3 2020",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 2\033[0m\nA data analyst has been asked to create an ad-hoc sales report for the Chief Executive Officer (CEO). Which of the following should be included in the report?\nA. The sales representatives' home addresses\nB. Line-item SKU numbers\nC. YTD total sales\nD. The customers' first and last names",
            "answer": "C"
        },
        {
            "question": "\033[1mQuestion 3\033[0m\nWhich of the following can be used to translate data into another form so it can only be read by a user who has a key or a password?\nA. Data encryption\nB. Data transmission\nC. Data protection\nD. Data masking",
            "answer": "A"
        },
        {
            "question": "\033[1mQuestion 4\033[0m\nWhich of the following is an example of a discrete data type?\nA. 8in (20cm)\nB. 5 kids\nC. 2.5mi (4km)\nD. 10.7lbs (4.9kg)",
            "answer": "B"
        },
        {
            "question": "\033[1mQuestion 5\033[0m\nWhich of the following contains alphanumeric values?\nA. 10.1Ε²\nB. 13.6\nC. 1347\nD. A3J7",
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
