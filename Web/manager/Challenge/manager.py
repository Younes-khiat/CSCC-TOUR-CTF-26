from flask import Flask, render_template_string, request, jsonify, send_file, redirect, url_for
import os
from pathlib import Path
from werkzeug.utils import secure_filename
import platform

app = Flask(__name__)

# Fixed main directory for file storage
MAIN_DIR = Path('file_storage')
MAIN_DIR.mkdir(exist_ok=True)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>File Manager</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; margin-bottom: 20px; }
        .controls { margin-bottom: 20px; display: flex; gap: 10px; flex-wrap: wrap; }
        button, input[type="submit"] { padding: 10px 15px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover, input[type="submit"]:hover { background: #0056b3; }
        input[type="text"], input[type="file"] { padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .breadcrumb { margin-bottom: 15px; color: #666; }
        .breadcrumb a { color: #007bff; text-decoration: none; }
        .breadcrumb a:hover { text-decoration: underline; }
        .file-list { list-style: none; }
        .file-item { padding: 12px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
        .file-item:hover { background: #f9f9f9; }
        .file-name { flex: 1; display: flex; align-items: center; gap: 10px; }
        .folder { color: #ffa500; font-weight: bold; }
        .file { color: #333; }
        .actions { display: flex; gap: 8px; }
        .actions button { padding: 5px 10px; font-size: 12px; }
        .btn-danger { background: #dc3545; }
        .btn-danger:hover { background: #c82333; }
        .btn-secondary { background: #6c757d; }
        .btn-secondary:hover { background: #5a6268; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; }
        .modal-content { background: white; margin: 100px auto; padding: 20px; width: 400px; border-radius: 8px; }
        .modal.active { display: block; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        .message { padding: 10px; margin-bottom: 15px; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📁 File Manager</h1>
        
        {% if message %}
        <div class="message {{ 'success' if success else 'error' }}">{{ message }}</div>
        {% endif %}
        
        <div class="breadcrumb">
            <a href="/">Home</a>
            {% for part in path_parts %}
                / <a href="?path={{ part.path }}">{{ part.name }}</a>
            {% endfor %}
        </div>
        
        <div class="controls">
            <button onclick="document.getElementById('uploadModal').classList.add('active')">📤 Upload File</button>
            <button onclick="document.getElementById('folderModal').classList.add('active')">📁 New Folder</button>
        </div>
        
        <ul class="file-list">
            {% for item in items %}
            <li class="file-item">
                <div class="file-name">
                    {% if item.is_dir %}
                        <span class="folder">📁</span>
                        <a href="?path={{ item.path }}">{{ item.name }}</a>
                    {% else %}
                        <span class="file">📄</span>
                        <span>{{ item.name }}</span>
                    {% endif %}
                </div>
                <div class="actions">
                    {% if not item.is_dir %}
                    <a href="/download?path={{ item.path }}"><button class="btn-secondary">⬇️ Download</button></a>
                    {% endif %}
                    <button class="btn-secondary" onclick="showMoveModal('{{ item.name }}', '{{ item.path }}', {{ 'true' if item.is_dir else 'false' }})">📦 Move</button>
                    <button class="btn-secondary" onclick="showCopyModal('{{ item.name }}', '{{ item.path }}', {{ 'true' if item.is_dir else 'false' }})">📋 Copy</button>
                    <form method="POST" action="/delete" style="display: inline;">
                        <input type="hidden" name="path" value="{{ item.path }}">
                        <button type="submit" class="btn-danger" onclick="return confirm('Delete {{ item.name }}?')">🗑️ Delete</button>
                    </form>
                </div>
            </li>
            {% endfor %}
            {% if not items %}
            <li class="file-item">Empty folder</li>
            {% endif %}
        </ul>
    </div>

    <!-- Upload Modal -->
    <div id="uploadModal" class="modal">
        <div class="modal-content">
            <h2>Upload File</h2>
            <form method="POST" action="/upload" enctype="multipart/form-data">
                <input type="hidden" name="current_path" value="{{ current_path }}">
                <div class="form-group">
                    <label>Select File:</label>
                    <input type="file" name="file" required>
                </div>
                <button type="submit">Upload</button>
                <button type="button" onclick="document.getElementById('uploadModal').classList.remove('active')">Cancel</button>
            </form>
        </div>
    </div>

    <!-- New Folder Modal -->
    <div id="folderModal" class="modal">
        <div class="modal-content">
            <h2>Create Folder</h2>
            <form method="POST" action="/create_folder">
                <input type="hidden" name="current_path" value="{{ current_path }}">
                <div class="form-group">
                    <label>Folder Name:</label>
                    <input type="text" name="folder_name" required>
                </div>
                <button type="submit">Create</button>
                <button type="button" onclick="document.getElementById('folderModal').classList.remove('active')">Cancel</button>
            </form>
        </div>
    </div>

    <!-- Move Modal -->
    <div id="moveModal" class="modal">
        <div class="modal-content">
            <h2>Move <span id="moveItemName"></span></h2>
            <form method="POST" action="/move">
                <input type="hidden" name="source" id="moveSource">
                <div class="form-group">
                    <label>Destination Folder:</label>
                    <select name="destination" id="moveDestination">
                        <option value="">/ (root)</option>
                        {% for folder in all_folders %}
                        <option value="{{ folder.path }}">{{ folder.display }}</option>
                        {% endfor %}
                    </select>
                </div>
                <button type="submit">Move</button>
                <button type="button" onclick="document.getElementById('moveModal').classList.remove('active')">Cancel</button>
            </form>
        </div>
    </div>

    <!-- Copy Modal -->
    <div id="copyModal" class="modal">
        <div class="modal-content">
            <h2>Copy <span id="copyItemName"></span></h2>
            <form method="POST" action="/copy">
                <input type="hidden" name="source" id="copySource">
                <div class="form-group">
                    <label>Destination Folder:</label>
                    <select name="destination" id="copyDestination">
                        <option value="">/ (root)</option>
                        {% for folder in all_folders %}
                        <option value="{{ folder.path }}">{{ folder.display }}</option>
                        {% endfor %}
                    </select>
                </div>
                <button type="submit">Copy</button>
                <button type="button" onclick="document.getElementById('copyModal').classList.remove('active')">Cancel</button>
            </form>
        </div>
    </div>

    <script>
        function showMoveModal(name, path, isDir) {
            document.getElementById('moveItemName').textContent = name;
            document.getElementById('moveSource').value = path;
            document.getElementById('moveModal').classList.add('active');
        }

        function showCopyModal(name, path, isDir) {
            document.getElementById('copyItemName').textContent = name;
            document.getElementById('copySource').value = path;
            document.getElementById('copyModal').classList.add('active');
        }
    </script>
</body>
</html>
'''

def get_all_folders(base_path=MAIN_DIR):
    """Recursively get all folders"""
    folders = []
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            full_path = Path(root) / d
            rel_path = full_path.relative_to(MAIN_DIR)
            folders.append({
                'path': str(rel_path),
                'display': '/' + str(rel_path)
            })
    return folders

@app.route('/')
def index():
    rel_path = request.args.get('path', '')
    current_dir = MAIN_DIR / rel_path
    
    if not current_dir.exists() or not current_dir.is_dir():
        current_dir = MAIN_DIR
        rel_path = ''
    
    items = []
    for item in sorted(current_dir.iterdir()):
        item_rel_path = item.relative_to(MAIN_DIR)
        items.append({
            'name': item.name,
            'path': str(item_rel_path),
            'is_dir': item.is_dir()
        })
    
    path_parts = []
    if rel_path:
        parts = Path(rel_path).parts
        for i, part in enumerate(parts):
            path_parts.append({
                'name': part,
                'path': str(Path(*parts[:i+1]))
            })
    
    all_folders = get_all_folders()
    message = request.args.get('message')
    success = request.args.get('success') == '1'
    
    return render_template_string(HTML_TEMPLATE, 
                                 items=items, 
                                 current_path=rel_path,
                                 path_parts=path_parts,
                                 all_folders=all_folders,
                                 message=message,
                                 success=success)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect('/?message=No file selected&success=0')
    
    file = request.files['file']
    if file.filename == '':
        return redirect('/?message=No file selected&success=0')
    
    current_path = request.form.get('current_path', '')
    upload_dir = MAIN_DIR / current_path
    
    filename = secure_filename(file.filename)
    file.save(upload_dir / filename)
    
    return redirect(f'/?path={current_path}&message=File uploaded successfully&success=1')

@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = secure_filename(request.form.get('folder_name', ''))
    current_path = request.form.get('current_path', '')
    
    if not folder_name:
        return redirect(f'/?path={current_path}&message=Invalid folder name&success=0')
    
    new_folder = MAIN_DIR / current_path / folder_name
    new_folder.mkdir(exist_ok=True)
    
    return redirect(f'/?path={current_path}&message=Folder created successfully&success=1')

@app.route('/download')
def download():
    file_path = request.args.get('path', '')
    full_path = MAIN_DIR / file_path
    
    if full_path.exists() and full_path.is_file():
        return send_file(full_path, as_attachment=True)
    
    return redirect('/?message=File not found&success=0')

@app.route('/delete', methods=['POST'])
def delete():
    item_path = request.form.get('path', '')
    full_path = MAIN_DIR / item_path
    
    if full_path.exists():
        # Use os.system with rm/rmdir commands
        if platform.system() == 'Windows':
            if full_path.is_dir():
                os.system(f'rmdir /s /q "{full_path}"')
            else:
                os.system(f'del /f /q "{full_path}"')
        else:  # Linux/Mac
            os.system(f'rm -rf "{full_path}"')
        
        parent_path = str(Path(item_path).parent) if Path(item_path).parent != Path('.') else ''
        return redirect(f'/?path={parent_path}&message=Deleted successfully&success=1')
    
    return redirect('/?message=Item not found&success=0')

@app.route('/move', methods=['POST'])
def move():
    source = request.form.get('source', '')
    destination = request.form.get('destination', '')
    
    source_path = MAIN_DIR / source
    dest_path = MAIN_DIR / destination / source_path.name
    
    if source_path.exists():
        # Use os.system with mv/move commands
        if platform.system() == 'Windows':
            os.system(f'move "{source_path}" "{dest_path}"')
        else:  # Linux/Mac
            os.system(f'mv "{source_path}" "{dest_path}"')
        
        return redirect(f'/?path={destination}&message=Moved successfully&success=1')
    
    return redirect('/?message=Source not found&success=0')

@app.route('/copy', methods=['POST'])
def copy():
    source = request.form.get('source', '')
    destination = request.form.get('destination', '')
    
    source_path = MAIN_DIR / source
    dest_path = MAIN_DIR / destination / source_path.name
    
    if source_path.exists():
        # Use os.system with cp/copy commands
        if platform.system() == 'Windows':
            if source_path.is_dir():
                os.system(f'xcopy "{source_path}" "{dest_path}" /e /i /h /y')
            else:
                os.system(f'copy "{source_path}" "{dest_path}"')
        else:  # Linux/Mac
            os.system(f'cp -r "{source_path}" "{dest_path}"')
        
        return redirect(f'/?path={destination}&message=Copied successfully&success=1')
    
    return redirect('/?message=Source not found&success=0')

if __name__ == '__main__':
    app.run(debug=True)
