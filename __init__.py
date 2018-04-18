import pandas as pd
import pprint
from flask import Flask, render_template, request, redirect
import model
from werkzeug.utils import secure_filename
app = Flask(__name__)

ALLOWED_EXTENSIONS = ['csv']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit ('.', 1)[1].lower () in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def lol():
   return render_template('test.html', failureMessage="Choose a Dataset ")


@app.route('/read', methods=['POST'])
def postFile():
    print("Entered Read")
    file = request.files["user_file"]
    print (file)
    if file.filename == "":
        print ("No Filename")
        return "Please select a file"
    if file and allowed_file (file.filename):
        print ("Proeper File")
        file.filename = secure_filename (file.filename)
        print ("here")
        print (file)

        df = pd.read_csv (file, encoding='cp1252')
        print("Read CSV")
        totalCorrectPrediction, lenghtOfTestSet, finalProbability, max1Lable, max2Lable, confusionMatrix = model.calculate (
            df)
        print("Done With the function")
        finalProbability = str(round (finalProbability *100, 4)) + "%"
        return render_template ('test.html', message="The Results Are: ",
                                totalCorrectPrediction=totalCorrectPrediction, lenghtOfTestSet=lenghtOfTestSet,
                                finalProbability=finalProbability,
                                max1Lable=max1Lable, max2Lable=max2Lable, confusionMatrix=confusionMatrix)

        # print ("The Exception is: ", e)
        # return render_template ('test.html', failureMessage="There is an Exception: ")
    else:
        return render_template ('test.html', failureMessage="Incorrect File Entered")


if __name__ == '__main__':
    app.run(debug=True)
