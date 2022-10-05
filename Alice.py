import socket
import random


def Com(m, r):
    return hash(f"{r}{m}")

def dieCalc(a, b):
    return ((int(a) ^ int(b)) % 6) + 1

def randBitStr(n):
    result = ""
    for _ in range(n):
        temp = str(random.randint(0, 1))
        result += temp
    return result


def test():
    # Select random Alice r
    aliceR = randBitStr(128)
    # Select random Alice message
    aliceM = randBitStr(8)

    # Select random Bob message
    bobM = randBitStr(8)

    print(f"Alice sends to Bob: {Com(aliceM, aliceR)}")
    bobSee = Com(aliceM, aliceR)
    print(f"\nBob sends to Alice: {bobM}")
    print(f"\nAlice sends to Bob: ({aliceM}, {aliceR})")
    print(f"\nBob checks if {bobSee == Com(aliceM, aliceR)}")
    print(f"\nComputation for them both: {dieCalc(bobM, aliceM)}")

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    test()