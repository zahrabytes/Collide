from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Flask server is running'})

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({'data': 'This is some data from the backend'})

@app.route('/data', methods=['POST'])
def post_data():
    data = request.json
    return jsonify({'status': 'Data received', 'data': data})

if __name__ == '__main__':
    app.run(debug=True)
