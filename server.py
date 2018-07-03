from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    content = request.json
    print(content)
    return jsonify({
        "status":"ok"
        })

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)