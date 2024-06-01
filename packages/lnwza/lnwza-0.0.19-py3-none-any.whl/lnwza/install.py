import os
import subprocess


def create_bat(venv_path, package_name, proxy_http=None):
    activate_bat_file = os.path.join(venv_path, r'Scripts\activate.bat')
    txt = f'@echo off\n'
    txt += f'call "{activate_bat_file}"\n'
    txt += f'pip install --proxy {proxy_http} {package_name}\n'
    with open('run.bat', 'w') as f:
        f.write(txt)
    print(os.listdir())


def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        print(f"error delete file {file_path}")


def install_package(venv_path, package_name):
    proxy_http = 'http://agyc026730:op90-===@150.61.8.70:10080'
    create_bat(venv_path, package_name, proxy_http)

    subprocess.run("run.bat", shell=True)

    delete_file('run.bat')


if __name__ == "__main__":
    install_package('numpy')
