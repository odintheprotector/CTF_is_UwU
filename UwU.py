#CTF challenge
from multiprocessing import Process
from multiprocessing import set_start_method
import threading


secret_data = ["this", "is", "magic", "word"]
index = 0
key = ""
threads = []


def child_task(a, b):
    global secret_data

    secret_data[a], secret_data[b] = secret_data[b], secret_data[a]
    secret = "".join(secret_data)
    with open("password.enc", "w") as f:
        f.write(secret)


def create_child_process():
    set_start_method('fork')
    process = Process(target=child_task, args=(2, 3,))
    process.start()


def generate_key(vector):
    global key_string
    global index
    global key

    for _ in range(10):
        index += 1
        key_string += key_string[index]
        print(index)

        if index == vector:
            key = ''.join(key_string)


def get_password():
    with open("password.enc", "r") as f:
        password = f.read()

    return password


def encrypt_flag(key):
    print(f"Encrypting flag with key: {key}")

    with open("flag.txt", "rb") as f:
        data = f.read()

    flag = ""
    for i in range(len(data)):
        flag += chr(data[i] ^ ord(key[i]))

    return flag


def main():
    global secret_data

    create_child_process()
    secret = "".join(secret_data)
    with open("password.txt", "w") as f:
        f.write(secret)
    while True:
        try:
            system_password = get_password()
            if len(system_password) != 15:
                continue
            break
        except Exception as _:
            pass

    user_input_password = input("What is my magic word: ")

    if user_input_password == system_password:
        vector = int(input("Give me a number: "))
        for _ in range(4):
            t = threading.Thread(target=generate_key, args=(vector,))
            t.start()
            threads.append(t)
    else:
        print("Invalid password")
        exit()

    for t in threads:
        t.join()

    data = encrypt_flag(key)
    with open("flag.enc", "wb") as f:
        f.write(data.encode())


if __name__ == '__main__':
    main()
