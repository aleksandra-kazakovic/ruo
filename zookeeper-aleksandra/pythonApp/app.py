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
        epochs = request.form.get("epochs", default=20, type=int)
        batch_size = request.form.get("batch_size", default=10, type=int)

        if y_col is None:
            return "The output column must be entered in the y_col field."
        if model_name is None:
            return "Model_name is a required field. The model name can be any text."

        ann = ANN()
        print("Epocha "+model_name+"  "+y_col+"   "+str(epochs)+"*****")
        guid, acc, auc = ann.train_model(file_path, y_col, epochs, batch_size)
        if(guid == 'non'):
            return "the model cannot be trained"
        db.insert_model(model_name, guid, os.path.join("models", guid + ".h5"), acc, auc)
        return "Ok"

    return False


@app.route('/getListOfModels')
def models():
    return json.dumps(db.get_models(),  default=lambda o: o.__dict__,
            sort_keys=False, indent=4)



@app.route('/delete/<int:id>/', methods=['GET'])
def delete_model(id):
    model = db.get_model_by_id(id)
    if os.path.exists(model.modelPath):
        os.remove(model.modelPath)
    db.delete_model_by_id(id)
    return "Ok"


@app.route('/modelSummary', methods=['POST'])
def model_summary():
    file_path = request.form.get('file_path')
    if os.path.exists(file_path):
         ann = ANN()
         return ann.model_summary(file_path)
    return "File dont exist"
         


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
        if model_guid is None:
            return "Model_guid is a required field."
        ann = ANN()
        predictions = ann.predict_value(model_guid, file_path)

        print(predictions)
        if (isinstance(predictions, int)):
            return "Some error in prediction. Check if the file is correct. The prediction file should not have an output column."
        i = 1
        pred_dict = dict()
        for prediction in predictions:
            pred_dict['prediction_' + str(i)] = float(prediction[0])                                  
            i += 1

        return jsonify(pred_dict)


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0',debug=True,port='5000')