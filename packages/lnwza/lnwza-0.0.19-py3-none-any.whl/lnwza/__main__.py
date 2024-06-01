# import os
# import sys
# from . import proxy, install
#
# if __name__ == '__main__':
#
#     # file_path = __file__
#     # print('file_path', file_path)
#
#     current_path = os.getcwd()
#     print('current_path', current_path)
#     # how to get current path
#
#     if len(sys.argv) > 1:
#         if sys.argv[1] == 'proxy':
#             # r get
#             if len(sys.argv) == 3 and sys.argv[2] == 'get':
#                 proxy.get()
#
#             # r set proxy_host xxx.xxx.x.x
#             if len(sys.argv) == 5 and sys.argv[2] == 'set':
#                 proxy.set(sys.argv[3], sys.argv[4])
#
#     # r install x
#     if len(sys.argv) == 3 and sys.argv[1] == 'install':
#         print(sys.argv[1:])
#         package_name = sys.argv[2]
#         install.install_package(package_name)
