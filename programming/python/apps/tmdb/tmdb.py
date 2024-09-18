import requests
import pandas as pd

# Function to fetch movie data based on user's mood
def fetch_movies_by_mood(mood, api_key, do_not_show, recommended_movies):
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        'api_key': api_key,
        'language': 'en-US',
        'sort_by': 'popularity.desc',
        'include_adult': 'false',
        'with_genres': get_genre_id(mood, api_key),
        'page': 1
    }
    
    # Fetching the first page of results
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()['results']
        total_pages = response.json()['total_pages']
        
        # Fetching subsequent pages of results until we have enough movies
        page = 2
        while len(results) < 50 and page <= total_pages:
            params['page'] = page
            response = requests.get(url, params=params)
            if response.status_code == 200:
                results.extend(response.json()['results'])
                page += 1
            else:
                print(f"Failed to fetch page {page} of data from TMDb API")
                break
        
        # Filter out movies in the do_not_show list and already recommended
        filtered_results = [movie for movie in results if movie['title'].strip().lower() not in map(str.strip, map(str.lower, do_not_show)) and movie['title'] not in recommended_movies]
        
        return filtered_results[:50]  # Return at most 50 movies
    else:
        print("Failed to fetch data from TMDb API")
        return None

# Function to get genre ID based on mood
def get_genre_id(mood, api_key):
    # Dictionary mapping moods to genre IDs
    mood_to_genre = {
        'happy': 35,  # Comedy
        'sad': 18,    # Drama
        'action': 28, # Action
        'scary': 27,  # Horror
        'romantic': 10749, # Romance
    }
    return mood_to_genre.get(mood.lower(), 18)  # Default to Drama if mood not found

# Function to recommend movies
def recommend_movies(mood, api_key, do_not_show, recommended_movies):
    movies = fetch_movies_by_mood(mood, api_key, do_not_show, recommended_movies)
    if movies:
        df = pd.DataFrame(movies)
        recommended_titles = df['title'].tolist()
        recommended_movies.extend(recommended_titles)
        # Truncate overview to 5 words or less
        df['overview'] = df['overview'].apply(lambda x: ' '.join(x.split()[:5]) + '...' if len(x.split()) > 5 else x)
        return df[['title', 'vote_average', 'release_date', 'overview']]
    else:
        return None

# Function to save do not show list to a file
def save_do_not_show_list(do_not_show):
    with open("do_not_show.txt", "w") as file:
        for movie in do_not_show:
            file.write(movie + "\n")

# Function to load do not show list from a file
def load_do_not_show_list():
    try:
        with open("do_not_show.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

# Function to list all movies in the do not show list and allow the user to remove a movie
def list_and_remove_movies(do_not_show):
    print("Movies in the 'Don't Recommend' list:")
    for i, movie in enumerate(do_not_show, 1):
        print(f"{i}. {movie}")
    print("0. Done removing movies")
    while True:
        choice = input("Choose an option:\n1. Show the removed list\n2. Remove another movie and add to removed list\n3. Show recommendations\nEnter choice: ")
        if choice == '1':
            if not do_not_show:
                print("No movies in the 'Don't Recommend' list.")
            else:
                print("Movies in the 'Don't Recommend' list:")
                for i, movie in enumerate(do_not_show, 1):
                    print(f"{i}. {movie}")
        elif choice == '2':
            movie_title = input("Enter the title of the movie you want to remove and add to the 'Don't Recommend' list: ")
            do_not_show.append(movie_title)
            print(f"'{movie_title}' has been added to the 'Don't Recommend' list.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Main function
def main():
    api_key = "your-api"
    mood = input("Enter your mood (happy, sad, action, scary, romantic): ")
    
    # Load do not show list from file
    do_not_show = load_do_not_show_list()
    
    # List and remove movies from the do not show list
    list_and_remove_movies(do_not_show)
    
    # Save updated do not show list to file
    save_do_not_show_list(do_not_show)
    
    # Initialize recommended movies list
    recommended_movies = []
    
    # Get recommendations
    recommended_movies_df = recommend_movies(mood, api_key, do_not_show, recommended_movies)
    if recommended_movies_df is not None:
        print("\033[1m\033[91mHere are recommended movies for your mood:\033[0m")
        print(recommended_movies_df.to_string(index=False))
    else:
        print("Failed to get recommendations.")

if __name__ == "__main__":
    main()
