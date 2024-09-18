from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

def init_db():
    db_path = os.path.join(app.instance_path, "notes.db")
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT NOT NULL)")
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    content = request.form["content"]
    if content:
        try:
            new_note = Notes(content=content)
            db.session.add(new_note)
            db.session.commit()
            return jsonify({"status": "success", "message": "Note saved successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"Error saving note: {str(e)}"})
    else:
        return jsonify({"status": "error", "message": "Cannot save an empty note."})

@app.route("/clear", methods=["POST"])
def clear():
    try:
        Notes.query.delete()
        db.session.commit()
        return jsonify({"status": "success", "message": "All notes cleared successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Error clearing notes: {str(e)}"})

@app.route("/load", methods=["GET"])
def load():
    try:
        note = Notes.query.order_by(Notes.id.desc()).first()
        content = note.content if note else ""
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error loading note: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4444))
    app.run(host="0.0.0.0", port=port, debug=True)
