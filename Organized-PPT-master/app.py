import os
#import magic
import urllib.request
#from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import notesprocessing as notepro

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload'

ALLOWED_EXTENSIONS = set(['pptx','pptm','potx','potm','ppsx','ppam','ppsm','sldx'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/generate", methods =["POST"])
def gen():
    #start = time.time()
    print("hi")
    if request.method == 'POST':
        # if 'files[]' not in request.files:
        #     return redirect(request.url)
        file = request.files.getlist('file[]')
        for file1 in file:
            #if file1 and allowed_file(file1.filename):
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename)))
   
    #savenotepro.essen()
    notepro.essen2()
    return render_template('finalhtmlfile.html')
@app.route("/links")
def links():
    return render_template(
        "finalhtmlfile.html",
        trigger=True
        )

    
    
        
            

     
    #infile = 'input.txt'
    # #outfile = 'output.txt'
    # file = open(infile, 'r', encoding='utf-8')
    # text = file.read()
    # n=int(request.form['num_of_ques'])
    # # n=3
    # questions = qgen.generateQuestions(text,n)
    # #end = time.time()
    # #final_time = end - start
    # #print(final_time)
    # return jsonify(questions)


if __name__ == '__main__':
    app.run(debug=True)