from flask import Flask, render_template, request, abort
import os
import mimetypes
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import HtmlFormatter

app = Flask(__name__)

EXCLUDED_FOLDERS = ['/mnt/c/study/Credentials']

def is_excluded(path):
    return any(path.startswith(excluded) for excluded in EXCLUDED_FOLDERS)

@app.route('/')
def index():
    path = request.args.get('path', '/mnt/c/study')
    if is_excluded(path):
        abort(403)
    items = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if not is_excluded(full_path):
            is_dir = os.path.isdir(full_path)
            items.append({'name': item, 'is_dir': is_dir, 'path': full_path})
    return render_template('index.html', items=items, current_path=path)

@app.route('/view')
def view_file():
    file_path = request.args.get('path')
    if is_excluded(file_path):
        abort(403)
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith('text'):
                try:
                    lexer = get_lexer_for_filename(file_path)
                except:
                    lexer = TextLexer()
                formatter = HtmlFormatter(style='monokai', linenos=True, cssclass="source")
                highlighted_content = highlight(content, lexer, formatter)
                css = formatter.get_style_defs('.source')
            else:
                highlighted_content = f"<pre>{content}</pre>"
                css = ""
            
            return render_template('view.html', content=highlighted_content, file_path=file_path, css=css)
        except UnicodeDecodeError:
            return "This file cannot be displayed as text.", 415
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
