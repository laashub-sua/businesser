import platform

if __name__ == '__main__':
    if platform.system() != "Windows":
        print('not windows')
