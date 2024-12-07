import subprocess

# 定义脚本路径
download_script = r"download.py"
analysis_script = r"analysis.py"
pic_script = r"pic.py"

# 运行 download.py
print("Running download.py...")
result = subprocess.run(['python', download_script], check=True)
print(f"download.py exited with code {result.returncode}")

# 运行 analysis.py
print("Running analysis.py...")
result = subprocess.run(['python', analysis_script], check=True)
print(f"analysis.py exited with code {result.returncode}")

# 运行 pic.py
print("Running pic.py...")
result = subprocess.run(['python', pic_script], check=True)
print(f"pic.py exited with code {result.returncode}")



