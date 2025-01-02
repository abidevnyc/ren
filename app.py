from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def get_pwd():

    current_directory = os.getcwd()
    return jsonify({"current_directory": current_directory})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
