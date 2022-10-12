import socket
import time
import Utility
from ssl import CERT_REQUIRED, SSLContext, PROTOCOL_TLS_SERVER

# Acts as server for Alice
def server_program():
    host = socket.gethostname()
    port = 5001

    # Set SSL Context as server. Verify mode is CERT_REQUIRED, which means client must also have cert.
    context = SSLContext(PROTOCOL_TLS_SERVER)
    context.verify_mode = CERT_REQUIRED

    # Load Bob cert and key, and store location of Alice cert
    context.load_cert_chain('bobCert.pem', 'bobKey.pem')
    context.load_verify_locations("aliceCert.pem")

    server = socket.socket()

    server.bind((host, port)) 
    server.listen()

    tls = context.wrap_socket(server, server_side=True)
    conn, address = tls.accept()

    print("Connection from: " + str(address))
    
    # Establish TSL is configured correctly
    clientCert = conn.getpeercert()
    print(f"client have cert: {clientCert != None}")

    shake = conn.do_handshake()
    print(f"handshake done: {shake == None}")

    a, b, c = conn.cipher()
    print(f"TLS cipher: {a, b, c}")
    
    print("\n======== PROTOCOL BEGINS ========\n")
    # Loop awaiting messages from Alice
    while True:
        # Receive aliceCom
        aliceCom = conn.recv(1024).decode()
        print(f"Commitment received from Alice: {aliceCom}")
        time.sleep(1)

        # Generate random message and send to Alice
        bobM = Utility.randDie()
        print("Sending dice result to Alice")
        time.sleep(1)
        conn.send(str(bobM).encode())

        # Receive r and m from Alice, and check if equal to each other.
        aliceR, aliceM = conn.recv(1024).decode().split(",")
        aliceTrustworthy = aliceCom == Utility.Com(aliceR, aliceM)
        print(f"Received r and m from Alice.\nCheck if Commitment from Alice is equal to Com(aliceR, aliceM): {aliceTrustworthy}")
        time.sleep(1)

        # If alice is trustworthy, calculate virtual dice result
        if aliceTrustworthy:
            print(f"---- Virtual dice is: {Utility.dieCalc(aliceM, bobM)}\n")
        else:
            print("Cannot roll virtual dice, as Alice is not trustworthy\n")

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
