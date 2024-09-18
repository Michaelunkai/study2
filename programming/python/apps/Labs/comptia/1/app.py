from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

# Load questions from a JSON file
with open('questions.json', 'r') as f:
    questions = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    question = random.choice(questions)
    return jsonify(question)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    question_id = data['question_id']
    user_answer = data['answer']
    
    for question in questions:
        if question['id'] == question_id:
            correct = question['correct_answer'] == user_answer
            return jsonify({
                'correct': correct,
                'explanation': question['explanation']
            })
    
    return jsonify({'error': 'Question not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
