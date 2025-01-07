from flask import Flask, render_template, request, send_file, abort
import os
import magic
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter

app = Flask(__name__)

@app.route('/')
def index():
    path = request.args.get('path', '/mnt/c/study')
    if not os.path.exists(path):
        abort(404)
    items = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        is_dir = os.path.isdir(full_path)
        items.append({'name': item, 'is_dir': is_dir, 'path': full_path})
    items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
    return render_template('index.html', items=items, current_path=path)

@app.route('/view')
def view_file():
    file_path = request.args.get('path')
    if not os.path.exists(file_path):
        abort(404)
    if os.path.isfile(file_path):
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        if file_type.startswith('text') or file_type in ['application/json', 'application/xml']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                try:
                    lexer = get_lexer_for_filename(file_path)
                except:
                    try:
                        lexer = guess_lexer(content)
                    except:
                        lexer = TextLexer()
                formatter = HtmlFormatter(style='monokai', linenos=True, cssclass="source")
                highlighted_content = highlight(content, lexer, formatter)
                css = formatter.get_style_defs('.source')
                return render_template('view.html', content=highlighted_content, file_path=file_path, css=css)
            except UnicodeDecodeError:
                return "This file cannot be displayed as text.", 415
        else:
            return send_file(file_path, as_attachment=True)
    else:
        return "Not a file", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)
