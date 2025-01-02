from flask import Flask, jsonify
import subprocess
import os

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

# 切换到 abc 目录并执行命令
@app.route('/run-in-abc', methods=['GET'])
def run_in_abc():
    try:
        # 获取当前目录
        current_directory = os.getcwd()
        
        # 检查 abc 目录是否存在
        if not os.path.isdir('abc'):
            return jsonify({"status": "error", "message": "'abc' directory does not exist"}), 400

        # 切换到 abc 目录并执行命令
        os.chdir('abc')
        # 你可以在这里执行更多命令，例：
        result = subprocess.run(["pwd"], capture_output=True, text=True)
        
        # 获取执行结果
        output = result.stdout.strip()

        # 返回切换目录后的输出
        return jsonify({
            "status": "success",
            "message": f"Switched to directory 'abc'. Current directory is: {output}"
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 主页路由
@app.route('/')
def home():
    return "Welcome to the Flask App!"

if __name__ == '__main__':
    # 运行 Flask 开发服务器
    app.run(host='0.0.0.0', port=5000, debug=True)
