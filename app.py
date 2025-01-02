import subprocess

# 检查 curl 是否可用
try:
    subprocess.run(["curl", "--version"], check=True, capture_output=True)
    print("curl is available")
except subprocess.CalledProcessError:
    print("curl is not available")

# 检查 tar 是否可用
try:
    subprocess.run(["tar", "--version"], check=True, capture_output=True)
    print("tar is available")
except subprocess.CalledProcessError:
    print("tar is not available")
