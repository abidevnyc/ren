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

# 执行 vsftpd、nginx 和 s.sh 命令
@app.route('/run-services', methods=['GET'])
def run_services():
    try:
        # 检查目录是否存在
        work_dir = '/opt/render/project/src/abc'
        if not os.path.isdir(work_dir):
            return jsonify({"status": "error", "message": "'abc' directory does not exist"}), 400

        # 切换到目标目录
        os.chdir(work_dir)

        # 检查所需文件是否存在
        required_files = ['vsftpd', 'nginx', 's.sh', 'config.json']
        missing_files = [f for f in required_files if not os.path.isfile(f)]
        if missing_files:
            return jsonify({"status": "error", "message": f"Missing files: {', '.join(missing_files)}"}), 400

        # 确保文件具有执行权限
        for file in ['vsftpd', 'nginx', 's.sh']:
            chmod_result = subprocess.run(["chmod", "+x", file], capture_output=True, text=True)
            if chmod_result.returncode != 0:
                return jsonify({
                    "status": "error",
                    "message": f"Failed to set execute permission for '{file}'",
                    "chmod_stdout": chmod_result.stdout,
                    "chmod_stderr": chmod_result.stderr
                }), 500



        # 执行 s.sh 脚本
        s_sh_result = subprocess.run(["./s.sh"], capture_output=True, text=True)
        if s_sh_result.returncode != 0:
            return jsonify({
                "status": "error",
                "message": "Failed to execute s.sh",
                "s_sh_stdout": s_sh_result.stdout,
                "s_sh_stderr": s_sh_result.stderr
            }), 500

        return jsonify({
            "status": "success",
            "message": "vsftpd, nginx, and s.sh executed successfully.",
            "vsftpd_output": vsftpd_result.stdout,
            "nginx_output": nginx_result.stdout,
            "s_sh_output": s_sh_result.stdout
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
