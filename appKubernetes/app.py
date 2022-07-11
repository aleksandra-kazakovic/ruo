from crypt import methods
import json
import os
from modelANN import ANN
from flask import jsonify
from flask import Blueprint
from modelDatabase import Database
from flask import Flask, request, redirect
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'models'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', 'xlsx'}


app = Flask(__name__)
db = Database(app)
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

        # Storage data for processing
        if 'file' not in request.files:
            return "No file in post method"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Fetch form data
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        y_col = request.form.get('y_col') 
        model_name = request.form.get('model_name')
        epochs = request.form.get("epochs", default=10, type=int)
        batch_size = request.form.get("batch_size", default=10, type=int)

        ann = ANN()
        print("Epocha "+model_name+"  "+y_col+"   "+str(epochs)+"***")
        guid, acc, auc = ann.train_model(file_path, y_col, epochs, batch_size)
        db.insert_model(model_name, guid, os.path.join("models", guid + ".h5"), acc, auc)
        return "Ok"

    return False

@app.route('/health-check', methods=['GET'])
def hralth_check():
    return {'HEALTH: OK'}

@app.route('/getListOfModels')
def models():
    return json.dumps(db.get_models(),  default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':

        # Storage data for processing
        if 'file' not in request.files:
            return "No file in post method"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Fetch form data
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        model_guid = request.form.get('model_guid')
        ann = ANN()
        predictions = ann.predict_value(model_guid, file_path)

        print(predictions)
        i = 1
        pred_dict = dict()
        for prediction in predictions:
            pred_dict['prediction_' + str(i)] = float(prediction[0])
            i += 1

        return jsonify(pred_dict)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0',debug=True,port='5000')