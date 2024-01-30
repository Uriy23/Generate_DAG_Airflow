import subprocess
import os

def transport_file():
    src = '.env'
    dst = 'dwh_yoshi_v1/dbt_transform'
    filename = os.path.basename(src)
    dst_file = os.path.join(dst, filename)
    os.rename(src, dst_file)

def start_DBT():
    #Предусмотреть возможность запуска с аргусментами full/not_full
    script_path = "dwh_yoshi_v1/dbt_transform/start_dbt.py"
    args = ["not_full", "auto"]
    subprocess.call(["python", script_path] + args)


def start_DBT_TASK():
    cmd_git_clone = 'git clone https://Chupakhin_uriy@bitbucket.org/s25-ds/dwh_yoshi_v1.git'
    subprocess.call(cmd_git_clone)
    transport_file()
    start_DBT()


