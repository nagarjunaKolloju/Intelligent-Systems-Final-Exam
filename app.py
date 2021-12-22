from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os
from skimage.io import imread, imshow
from PIL import Image
import glob
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="./templates")
app.config['UPLOAD_PATH'] = "uploads"
app.config['UPLOAD_PATH_MODEL'] = "models"


def featureExtractor():
    file = os.listdir(app.config["UPLOAD_PATH"])[0]
    image = Image.open("./uploads/"+file)
    new_image = image.resize((400, 400))
    file = "./uploads/"+file
    # new_image.save(file)
    image = imread(file, as_gray=True)
    features = np.reshape(image, (400*400))
    # featuresTemp = featuresTemp.tolist()
    return features


def getImageType(index):
    index = index[0]
    if index == 0:
        return "BOTTLE"
    elif index == 1:
        return "FAN"
    elif index == 2:
        return "PEN"


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/uploadimage", methods=["POST"])
def form():
    print("in")
    className = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")
        uploadedImage = request.files["file"]
        # uploadedModel = request.files["file"][1]
        imageName = secure_filename(uploadedImage.filename)
        # modelName = secure_filename(uploadedModel.filename)
        uploadedImage.save(os.path.join(
            app.config['UPLOAD_PATH'], imageName))
        # uploadedModel.save(os.path.join(
        #     app.config['UPLOAD_PATH'], modelName))
        # print(filename)
        # if imageName != "":
        # file = os.listdir(app.config["UPLOAD_PATH"])[1]
        # with open("./final_model.pkl", 'rb') as filePtr:
        #     features = featureExtractor()
        #     model = pickle.load(filePtr)
        #     index = model.predict(features.reshape(1, 160000))
        #     className = getImageType(index)
        #     # print(className)
        #     upload = "./uploads"
        #     for path in os.listdir(upload):
        #         full_path = os.path.join(upload, path)
        #         os.remove(full_path)
        return jsonify(name=className)


@app.route("/uploadmodel", methods=["POST"])
def form1():
    print("in")
    className = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")
        # uploadedImage = request.files["file"]
        uploadedModel = request.files["file"]
        # imageName = secure_filename(uploadedImage.filename)
        modelName = secure_filename(uploadedModel.filename)
        # uploadedImage.save(os.path.join(
        # app.config['UPLOAD_PATH'], imageName))
        uploadedModel.save(os.path.join(
            app.config['UPLOAD_PATH_MODEL'], modelName))
        # print(filename)
        # if imageName != "":
        # file = os.listdir(app.config["UPLOAD_PATH"])[1]
        models_path = os.path.abspath(app.config["UPLOAD_PATH_MODEL"])
        # print(models_path)
        # print(glob.glob(models_path + "/*"))
        model_path = glob.glob(models_path + "/*")[0]
        with open(model_path, 'rb') as filePtr:
            features = featureExtractor()
            model = pickle.load(filePtr)
            index = model.predict(features.reshape(1, 160000))
            className = getImageType(index)
            # print(className)
            upload = "./uploads"
            for path in os.listdir(upload):
                full_path = os.path.join(upload, path)
                os.remove(full_path)
            model = "./models"
        for path in os.listdir(model):
            full_path = os.path.join(model, path)
            os.remove(full_path)
        return jsonify(name=className)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
