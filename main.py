from flask import Flask, request, redirect, url_for, send_from_directory
from flask import render_template
from utils import DataFile
from werkzeug.utils import secure_filename
from os import path, remove, listdir
from time import sleep


class GlobalTextHandler:
    def __init__(self):
        self.df = DataFile('text.txt')
        self.text = self.df.read()
        self.id = 0
    
    def get_text(self):
        return self.text
    
    def get_id(self):
        return self.id

    def set_text(self, text):
        self.id += 1
        self.text = text
        self.df.write(text)


FILE_FOLDER = './media/files/'
app = Flask("Fast_Text")
app.config['UPLOAD_FOLDER'] = FILE_FOLDER
gt = GlobalTextHandler()
id_files = 0

@app.route('/', methods=['GET'])
def handle():
    list_files = [f for f in listdir(FILE_FOLDER) if path.isfile(path.join(app.config['UPLOAD_FOLDER'], f))]
    data = {"title": "Fast Send", "text": gt.get_text(), "files": list_files}
    template = render_template("index.html", data = data)
    return template


@app.route('/upload', methods=['POST'])
def upload():
    global id_files
    if request.method == 'POST':
        text = request.form["load_text"]
        gt.set_text(text)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                id_files += 1
    
    return redirect(url_for('handle'))


@app.route('/uploads/<path:filename>')
def download(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route('/delete/<path:filename>')
def delete(filename):
    global id_files
    file_path = path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        remove(file_path)
        id_files += 1
    except:
        pass
    return redirect(url_for('handle'))


@app.route('/api/versions')
def api_version():
    global id_files
    return {"id_text": gt.get_id(), "id_files": id_files}


@app.route('/api/data')
def api_data():
    list_files = [f for f in listdir(FILE_FOLDER) if path.isfile(path.join(app.config['UPLOAD_FOLDER'], f))]
    link_list = []
    for i in list_files:
        link_list.append({"name":i, "url": path.join('/uploads/', i)})
    return {"text": gt.get_text(), "files": link_list}


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    # убери потом debug
    # Debug ломает логику записи в файл!!!!!!!!!!!!!!
    sleep(3)
    app.run(debug=False, host='0.0.0.0', port=8080)
    

