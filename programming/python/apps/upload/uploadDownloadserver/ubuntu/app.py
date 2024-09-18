from flask import Flask, render_template, request, send_file, abort
import os
import shutil

UPLOAD_FOLDER = 'C:\Users\micha\Downloads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_files_and_directories(folder_path):
    items = os.listdir(folder_path)
    result = []
    for item in items:
        full_path = os.path.join(folder_path, item)
        result.append((item, os.path.isdir(full_path)))
    return result


@app.route('/')
def index():
    path = request.args.get('path', UPLOAD_FOLDER)
    files_and_directories = get_files_and_directories(path)
    return render_template('index.html', items=files_and_directories)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'File uploaded successfully'


def zip_folder(folder_path, zip_filename):
    shutil.make_archive(zip_filename, 'zip', folder_path)


@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            # Zip the folder and its contents
            zip_folder(file_path, file_path)
            return send_file(file_path + '.zip', as_attachment=True)
        else:
            return send_file(file_path, as_attachment=True)
    else:
        return abort(404)


@app.route('/browse')
def browse_directory():
    directory = request.args.get('directory')
    path = os.path.join(app.config['UPLOAD_FOLDER'], directory)
    if os.path.isdir(path):
        files_and_directories = get_files_and_directories(path)
        return render_template('index.html', items=files_and_directories)
    else:
        return abort(404)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.193')
