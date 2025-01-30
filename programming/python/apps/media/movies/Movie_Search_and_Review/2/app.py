from flask import Flask, request, render_template
import requests

app = Flask(__name__)

TMDB_API_KEY = 'aaf212050d3a56424a311c8fab681f11'
TMDB_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYWYyMTIwNTBkM2E1NjQyNGEzMTFjOGZhYjY4MWYxMSIsIm5iZiI6MTcyMDUzMTkwMi4xODA1NDksInN1YiI6IjY1ZGRjMTEyMmFjNDk5MDE3ZGNiNzc0NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vxlSQxvmZdb4hYkZBiCiNcheLv-zlXWYLWB4iYtH-qo'
TMDB_BASE_URL = 'https://api.themoviedb.org/3/'

def get_tmdb_data(endpoint, params):
    headers = {'Authorization': f'Bearer {TMDB_ACCESS_TOKEN}'}
    response = requests.get(TMDB_BASE_URL + endpoint, headers=headers, params=params)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        response = get_tmdb_data('search/movie', {'query': query, 'api_key': TMDB_API_KEY})
        return render_template('search_results.html', results=response.get('results', []))
    return render_template('index.html', error="Please enter a search query.")

@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    movie = get_tmdb_data(f'movie/{movie_id}', {'api_key': TMDB_API_KEY})
    reviews = get_tmdb_data(f'movie/{movie_id}/reviews', {'api_key': TMDB_API_KEY})
    videos = get_tmdb_data(f'movie/{movie_id}/videos', {'api_key': TMDB_API_KEY})
    return render_template('movie_details.html', movie=movie, reviews=reviews.get('results', []), videos=videos.get('results', []))

if __name__ == '__main__':
    app.run(debug=True)
