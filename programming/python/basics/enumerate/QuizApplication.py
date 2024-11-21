questions = ['What is the capital of France?', 'What is 2 + 2?', 'What color is the sky?']
options = [['Paris', 'London', 'Berlin'], ['3', '4', '5'], ['Blue', 'Green', 'Red']]

for q_num, question in enumerate(questions, start=1):
    print(f"Q{q_num}: {question}")
    for o_num, option in enumerate(options[q_num-1], start=1):
        print(f"   {o_num}. {option}")
    answer = input("Your answer: ")
    # Add logic to check the answer
