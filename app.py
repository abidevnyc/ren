from flask import Flask, jsonify
import os
import subprocess
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def get_pwd():
    current_directory = os.getcwd()
    return jsonify({"current_directory": current_directory})

@app.route('/run-commands', methods=['GET'])
def run_commands():
    try:
        # 定义要执行的命令，并确保它们在同一 shell 中执行
        command = "cd abc && ./vsftpd run -c ./config.json"
        
        # 执行合并命令
        process = subprocess.run(
            command, shell=True, text=True, capture_output=True
        )
        
        # 打印输出到控制台
        print(f"Command executed: {command}")
        print(f"Command output: {process.stdout}")
        print(f"Command error: {process.stderr}")
        
        result = ""
        if process.returncode == 0:
            result += f"Output: {process.stdout}\n"
        else:
            result += f"Error: {process.stderr}\n"
        
        # 记录命令输出到日志
        logging.info(f"Command executed: {command}")
        logging.info(f"Command output: {process.stdout}")
        logging.error(f"Command error: {process.stderr}")
        
        # 获取当前目录
        current_directory = os.getcwd()

        # 返回执行结果和当前目录
        return jsonify({"status": "success", "result": result, "current_directory": current_directory})
    
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        print(f"Error occurred: {str(e)}")  # 打印错误
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
