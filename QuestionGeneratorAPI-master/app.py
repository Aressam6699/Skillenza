from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import question_gen_run as qgen

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uplad/'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/generatequiz", methods =["POST"])
def gen():
    #start = time.time()

    file = request.files['file']
    file.save(secure_filename('input.txt'))

    infile = 'input.txt'
    #outfile = 'output.txt'
    file = open(infile, 'r', encoding='utf-8')
    text = file.read()
    n=int(request.form['num_of_ques'])
    # n=3
    questions = qgen.generateQuestions(text,n)
    #end = time.time()
    #final_time = end - start
    #print(final_time)
    return jsonify(questions)


if __name__ == '__main__':
    app.run(debug=False)

"""

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import os
import werkzeug
import question_gen_run as qgen
#from gensim.models import KeyedVectors
app = Flask(__name__)
api = Api(app)
UPLOAD_FOLDER = '/home/sam/Documents/train_flask/questiongen_API/question_generator-temp/uplad/'
parser = reqparse.RequestParser()
parser.add_argument('file',type=werkzeug.datastructures.FileStorage, location='files')


class quest(Resource):
    def post(self, num):
        data = parser.parse_args()
        upload = data['file']
        print()
        print(parser)
        print()
        if upload:
            filename = 'input.txt'
            upload.save(os.path.join(UPLOAD_FOLDER,filename))
        infile = 'input.txt'
        outfile = 'output.txt'
        file = open(infile, 'r', encoding='utf-8')
        text = file.read()
        n = num
        questions = qgen.generateQuestions(text,n)
        return {'about' : questions}


api.add_resource(quest, '/generatequiz/<int:num>')
# api.add_resource(Multi,'/multi/<int:num>')
    

if __name__ == '__main__':
    app.run(debug=True)
"""