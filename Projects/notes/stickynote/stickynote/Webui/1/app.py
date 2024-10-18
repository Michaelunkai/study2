from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

# Ensure database creation is within the application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    content = request.form['content']
    if content:
        new_note = Notes(content=content)
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Note saved successfully!'})
    else:
        return jsonify({'status': 'error', 'message': 'Cannot save an empty note.'})

@app.route('/clear', methods=['POST'])
def clear():
    Notes.query.delete()
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'All notes cleared successfully!'})

@app.route('/load', methods=['GET'])
def load():
    note = Notes.query.order_by(Notes.id.desc()).first()
    content = note.content if note else ""
    return jsonify({'content': content})

def auto_save_note():
    note_text = request.form['content']
    if note_text:
        new_note = Notes(content=note_text)
        db.session.add(new_note)
        db.session.commit()

scheduler = APScheduler()
scheduler.add_job(id='AutoSaveJob', func=auto_save_note, trigger='interval', seconds=5)
scheduler.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4444))
    app.run(host='0.0.0.0', port=port)

