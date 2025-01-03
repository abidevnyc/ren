from flask import Flask, jsonify
import subprocess
import os

# 创建 Flask 应用实例
app = Flask(__name__)

# 执行 vsftpd 命令
@app.route('/run-vsftpd', methods=['GET'])
def run_vsftpd():
    try:
        # 检查 abc 目录是否存在
        if not os.path.isdir('abc'):
            return jsonify({"status": "error", "message": "'abc' directory does not exist"}), 400

        # 切换到 abc 目录
        os.chdir('abc')

        # 检查 vsftpd 文件是否存在
        if not os.path.isfile('./vsftpd'):
            return jsonify({"status": "error", "message": "'vsftpd' executable not found"}), 400

        # 检查 config.json 文件是否存在
        if not os.path.isfile('./config.json'):
            return jsonify({"status": "error", "message": "'config.json' file not found"}), 400

        # 添加执行权限给 vsftpd
        chmod_result = subprocess.run(["chmod", "+x", "./vsftpd"], capture_output=True, text=True)
        if chmod_result.returncode != 0:
            return jsonify({
                "status": "error",
                "message": "Failed to set execute permission for 'vsftpd'",
                "chmod_error": chmod_result.stderr
            }), 500

        # 执行 vsftpd 命令
        vsftpd_result = subprocess.run(
            ["./vsftpd", "-c", "./config.json"],
            capture_output=True, text=True
        )

        # 检查 vsftpd 是否执行成功
        if vsftpd_result.returncode != 0:
            return jsonify({
                "status": "error",
                "message": "Failed to execute vsftpd",
                "vsftpd_error": vsftpd_result.stderr
            }), 500

        return jsonify({
            "status": "success",
            "message": "vsftpd executed successfully.",
            "vsftpd_output": vsftpd_result.stdout
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
