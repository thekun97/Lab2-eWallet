

def read_file():
    f = open("encryted_password.txt", "rb")
    line1 = f.readline()
    line2 = f.readline()
    print(line1, line2)


if __name__ == '__main__':
    read_file();