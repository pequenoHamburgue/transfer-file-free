from flask import Flask, request, render_template_string, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = None
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = '''
<!doctype html>
<title>Upload de Arquivo</title>
<h1>Enviar Arquivo limte 10MB</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Enviar>
</form>
'''

def is_allowed(filename):
    if ALLOWED_EXTENSIONS is None:
        return True
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    message = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            message = 'Nenhum arquivo enviado.'
        else:
            f = request.files['file']
            if f.filename:
                if is_allowed(f.filename):
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    message = f'Arquivo "{filename}" enviado com sucesso!'
                else:
                    message = 'Tipo de arquivo não permitido.'
            else:
                message = 'Nenhum arquivo selecionado.'
    
    return render_template_string(HTML + f"<p>{message}</p>")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
