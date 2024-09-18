from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Define the upload directory
UPLOAD_FOLDER = 'C:/Users/micha/Downloads'  # Update this with your desired upload path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST'])
def uploader():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        # Ensure the upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        # Save the file to the upload directory
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return 'File uploaded successfully'

if __name__ == '__main__':
    # Run the Flask app on both 192.168.1.178:5000 and 87.70.167.200:5000
    app.run(debug=True, host='0.0.0.0', port=5000)
