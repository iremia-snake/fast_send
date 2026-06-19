from flask import Flask, request, redirect, url_for, send_from_directory
from flask import render_template
from common_data import CommonTextHandler, CommonFilesHandler
from time import sleep
import os

app = Flask("Fast_Text")


app.config['UPLOAD_FOLDER'] = './media/files/'
os.makedirs(app.config['UPLOAD_FOLDER'])
f = open('./media/text.txt', mode='x')
f.close()
comText = CommonTextHandler('./media/text.txt')
comFiles = CommonFilesHandler('./media/files')


comText.read_file()


@app.route('/', methods=['GET'])
def handle():
    list_files = comFiles.get_list_files()
    text = comText.get_text()

    data = {"title": "Fast Send", "text": text, "files": list_files}

    template = render_template("index.html", data = data)
    return template


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        text = request.form["load_text"]
        comText.write(text)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                comFiles.add(file)
    
    return redirect(url_for('handle'))


@app.route('/uploads/<path:filename>')
def download(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route('/delete/<path:filename>')
def delete(filename):
    comFiles.remove_file(filename)
    return redirect(url_for('handle'))


@app.route('/api/versions')
def api_version():
    return {"id_text": comText.edit_id, "id_files": comFiles.edit_id}


@app.route('/api/data')
def api_data():
    list_files = comFiles.get_list_files()
    link_list = []
    for i in list_files:
        link_list.append({"name":i, "url": '/uploads/' + i})
    return {"text": comText.get_text(), "files": link_list}


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# if __name__ == '__main__':
#     sleep(3)
#     app.run(debug=False, host='0.0.0.0', port=8080)
    

