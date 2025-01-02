from flask import Flask, jsonify
import subprocess

# 创建 Flask 应用实例
app = Flask(__name__)

# 检查 curl 是否可用
@app.route('/check-curl', methods=['GET'])
def check_curl():
    try:
        subprocess.run(["curl", "--version"], check=True, capture_output=True)
        return jsonify({"status": "success", "message": "curl is available"})
    except subprocess.CalledProcessError:
        return jsonify({"status": "error", "message": "curl is not available"})

# 检查 tar 是否可用
@app.route('/check-tar', methods=['GET'])
def check_tar():
    try:
        subprocess.run(["tar", "--version"], check=True, capture_output=True)
        return jsonify({"status": "success", "message": "tar is available"})
    except subprocess.CalledProcessError:
        return jsonify({"status": "error", "message": "tar is not available"})

# 主页路由
@app.route('/')
def home():
    return "Welcome to the Flask App!"

if __name__ == '__main__':
    # 运行 Flask 开发服务器
    app.run(host='0.0.0.0', port=5000, debug=True)
