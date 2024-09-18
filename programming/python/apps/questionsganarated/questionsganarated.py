import random

# Define your exam questions and answers
questions_answers = {
    "What is the capital of France?": "Paris",
    "What is the largest planet in our solar system?": "Jupiter",
    "Who wrote the play 'Romeo and Juliet'?": "William Shakespeare",
    # Add more questions and answers as needed
}

def generate_question():
    # Randomly select a question from the dictionary
    question = random.choice(list(questions_answers.keys()))
    return question

def main():
    print("Welcome to the Exam!")

    while True:
        question = generate_question()
        print("\nQuestion:", question)

        answer = input("Your answer: ").lower()  # Convert user input to lowercase

        if answer == questions_answers[question].lower():  # Convert answer to lowercase for comparison
            print("Correct!")
        else:
            print(f"Wrong! The correct answer is: {questions_answers[question]}")

        proceed = input("Do you want to continue? (yes/no): ").lower()
        if proceed != 'yes':
            break

    print("Thank you for taking the Exam!")

if __name__ == "__main__":
    main()
