from flask import Flask, request, jsonify
import base64
import time
import os
import subprocess
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



predict_command = "python label_image.py \
--graph=output_graph.pb --labels=output_labels.txt \
--input_layer=Placeholder \
--output_layer=final_result \
--input_height=299 --input_width=299 \
--image=temp/{}"



def handle_file(file_content):
    filename = "".join(str(time.time()).split(".")) + ".jpg"
    attributes = file_content.split(";")
    file_name = attributes[1].split("name=")[-1]
    file_content = base64.b64decode(attributes[-1].split(",")[-1])
    with open("temp/" + filename , "wb") as file:
        file.write(file_content)
    return filename

@app.route('/predict', methods=['POST'])
@cross_origin()
def main():
    content = request.json["image"]
    filename = handle_file(content)
    output = subprocess.check_output(predict_command.format(filename), shell=True).decode("utf-8").split("\n")
    return jsonify({
        "child": float(output[0].split(" ")[1]),
        "abstract": float(output[1].split(" ")[1])
        })

@app.route('/')
def test():
    return jsonify({
        "status": "ok"
        })



if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)