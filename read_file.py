

def read_file():
    f = open("data/encryted_password.txt", "rb")
    line1 = f.readline()
    f.close()

    f = open("data/nonce.txt", "rb")
    line2 = f.readline()
    f.close()

    return line1, line2
