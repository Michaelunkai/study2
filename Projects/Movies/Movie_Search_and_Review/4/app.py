from flask import Flask, request, jsonify, render_template
import requests
import pandas as pd
import gzip

app = Flask(__name__)
from flask_cors import CORS
CORS(app)

TMDB_API_KEY = 'aaf212050d3a56424a311c8fab681f11'
TMDB_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYWYyMTIwNTBkM2E1NjQyNGEzMTFjOGZhYjY4MWYxMSIsIm5iZiI6MTcyMDUzMTkwMi4xODA1NDksInN1YiI6IjY1ZGRjMTEyMmFjNDk5MDE3ZGNiNzc0NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vxlSQxvmZdb4hYkZBiCiNcheLv-zlXWYLWB4iYtH-qo'
TMDB_BASE_URL = 'https://api.themoviedb.org/3/'

# Load IMDb ratings dataset
def load_imdb_ratings(file_path):
    with gzip.open(file_path, 'rt') as f:
        return pd.read_csv(f, sep='\t')

imdb_ratings = load_imdb_ratings('C:/study/programming/python/apps/movies/Movie_Search_and_Review/4/title.ratings.tsv.gz')

def get_tmdb_data(endpoint, params):
    headers = {'Authorization': f'Bearer {TMDB_ACCESS_TOKEN}'}
    response = requests.get(TMDB_BASE_URL + endpoint, headers=headers, params=params)
    return response.json()

def get_imdb_rating(imdb_id):
    rating_info = imdb_ratings[imdb_ratings['tconst'] == imdb_id]
    if not rating_info.empty:
        return rating_info.iloc[0]['averageRating']
    return None

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
    imdb_id = movie.get('imdb_id')
    imdb_rating = get_imdb_rating(imdb_id) if imdb_id else 'N/A'
    reviews = get_tmdb_data(f'movie/{movie_id}/reviews', {'api_key': TMDB_API_KEY})
    videos = get_tmdb_data(f'movie/{movie_id}/videos', {'api_key': TMDB_API_KEY})
    return render_template('movie_details.html', movie=movie, reviews=reviews.get('results', []), videos=videos.get('results', []), imdb_rating=imdb_rating)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query')
    if query:
        response = get_tmdb_data('search/keyword', {'query': query, 'api_key': TMDB_API_KEY})
        suggestions = [result['name'] for result in response.get('results', [])]
        return jsonify(suggestions)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
