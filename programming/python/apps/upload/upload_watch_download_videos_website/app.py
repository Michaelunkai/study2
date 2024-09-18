from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'

def get_uploaded_videos():
    uploaded_videos = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.mp4'):  # Assuming only .mp4 files are uploaded
            uploaded_videos.append(filename)
    return uploaded_videos

@app.route('/')
def index():
    uploaded_videos = get_uploaded_videos()
    return render_template('index.html', uploaded_videos=uploaded_videos)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))

@app.route('/watch/<filename>')
def watch(filename):
    return render_template('watch.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/remove', methods=['POST'])
def remove():
    filename = request.form['filename']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



