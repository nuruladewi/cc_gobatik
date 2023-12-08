from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["ALLOWED_EXTENSIONS"] = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return"." in filename and filename.split(".", 1)[1] in app.config["ALLOWED_EXTENSIONS"]

model = load_model("contohmodel.h5", compile=False)
with open("label.txt", "r") as file:
    labels = file.read().splitlines()

@app.route("/", methods=["GET"])
def index():
    return jsonify({
      "status": {
            "code": 200,
            "message": "Success fetching the API",
        },
        "data": None
    }), 200

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    if request.method == "POST":
        image = request.files["image"]
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            # locate your files save
            image.save("static/uploads/", filename)
            return "Saved"
        else:
            return jsonify({
                "status": {
                    "code": 400,
                    "message": "Client side error"
                },
                "data": None
            }), 400
    else:
        return jsonify({
            "status": {
                "code": 405,
                "message": "Method not allowed",
            },
            "data": None
        }), 405

# @app.route("/store_image", methods=["POST"])
# def store_image():
#     return jsonify({

#     })

if __name__ == '__main__':
    app.run(debug=True)