from ast import arg
from crypt import methods
import json
import os
from modelANN import ANN
from flask import jsonify
from flask import Blueprint
from flask import Flask, request, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'models'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', 'xlsx'}


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

#swagger specific 
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python-Ml"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


REQUEST_API = Blueprint('request_api', __name__)
app.register_blueprint(REQUEST_API)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/trainMlModel', methods=['POST'])
def train():
    if request.method == 'POST':
        print("Train model")
        args = request.args
        file_name = args.get('file_name')
        print(file_name)
        epochs = args.get("epochs", default=40, type=int)
        batch_size = args.get("batch_size", default=64, type=int)

        ann = ANN()
        respons = ann.train_model(file_name, epochs, batch_size)
        return respons

    return False

@app.route('/health-check', methods=['GET'])
def hralth_check():
    return {'HEALTH: OK'}


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        print("Predikcija modela")
        args = request.args
        model_name = args.get('model_name')
        dataset_name = args.get('dataset_name')
        print(model_name)
        print(dataset_name)
        ann = ANN()
        predictions = ann.predict_value(model_name, dataset_name)

        print(predictions)
        if (isinstance(predictions, int)):
            return "No file on s3"
        i = 1
        pred_dict = dict()
        for prediction in predictions:
            pred_dict['prediction_' + str(i)] = float(prediction[0])
            i += 1

        return jsonify(pred_dict)

@app.route('/delete', methods=['POST'])
def delete_model():
    
    try:
       # model_name = request.form.get('model_name')
        model_name = request.args.get('model_name')
        print(model_name)
        ann = ANN()
        ann.delete(model_name)
        return "Deleted"
    except Exception as e:
        return "Bad request"
    

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',debug=True,port='5000')