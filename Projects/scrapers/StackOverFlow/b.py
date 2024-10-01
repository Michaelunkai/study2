import requests

def get_stackoverflow_results(query):
    url = "https://api.stackexchange.com/2.3/search/advanced"
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error: Unable to fetch results (status code {response.status_code})")
        return []

def get_answers(question_id):
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "filter": "withbody"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error: Unable to fetch answers (status code {response.status_code})")
        return []

def display_answers(answers):
    print("\n\033[91m" + "Answers:" + "\033[0m")  # Big red title
    for answer in answers:
        score = answer.get('score')
        body = answer.get('body')
        print(f"\nScore: {score}")
        print(f"Answer: {body}")
        print("_" * 50)

def main():
    query = input("Enter your search query: ")
    results = get_stackoverflow_results(query)

    if not results:
        print("No results found.")
        return

    for i, result in enumerate(results, 1):
        title = result.get('title')
        link = result.get('link')
        question_id = result.get('question_id')
        print(f"{i}. Title: {title}")
        print(f"   Link: {link}")
        print(f"   To see answers, type 'answers {i}'")

    while True:
        command = input("\nEnter command (or 'exit' to quit): ").strip().lower()
        if command == 'exit':
            break
        elif command.startswith('answers '):
            try:
                index = int(command.split()[1]) - 1
                if 0 <= index < len(results):
                    question_id = results[index].get('question_id')
                    answers = get_answers(question_id)
                    if not answers:
                        print("No answers found.")
                    else:
                        display_answers(answers)
                else:
                    print("Invalid question number.")
            except (IndexError, ValueError):
                print("Invalid command format. Use 'answers <number>'.")
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()