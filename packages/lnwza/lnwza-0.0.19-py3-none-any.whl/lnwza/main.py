import os
import sys
from . import proxy, install


def main():
    # current_path = os.getcwd()
    # print('current_path', current_path)

    if len(sys.argv) > 1:
        if sys.argv[1] == 'proxy':
            # r set proxy_host xxx.xxx.x.x
            if len(sys.argv) == 5 and sys.argv[2] == 'set':
                proxy.set(sys.argv[3], sys.argv[4])
        proxy.get()

    # r install <package_name>
    if len(sys.argv) == 3 and sys.argv[1] == 'install':
        package_name = sys.argv[2]

        dir_ = os.path.dirname(__file__)
        while True:
            if 'Scripts' in os.listdir(dir_):
                print(dir_)
                break
            else:
                dir_ = os.path.split(dir_)[0]

        install.install_package(dir_, package_name)


if __name__ == '__main__':
    main()

