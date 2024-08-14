from env import APP_KITS_FOLDER
import subprocess


def run_git(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Success: {result.stdout}")
    else:
        print(f"Error: {result.stderr}")


def run():
    command = f"cd {APP_KITS_FOLDER} && git add . && git commit -m 'new kit' && git push origin main"
    print(f'Running: {command}')
    run_git(command)

