import requests

def search_github_repos(query):
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        repositories = data['items'][:20]  # Get the top 20 repositories
        for index, repo in enumerate(repositories, start=1):
            print(f"{index}. {repo['name']} by {repo['owner']['login']}")
            print(f"   Description: {repo['description']}")
            print(f"   URL: {repo['html_url']}")
            print(f"   Stars: {repo['stargazers_count']}")
            print(f"   Forks: {repo['forks_count']}")
            print(f"   Language: {repo['language']}")
            print()
    else:
        print("Failed to retrieve data from GitHub.")

def main():
    search_query = input("Enter your search query: ")
    search_github_repos(search_query)

if __name__ == "__main__":
    main()
