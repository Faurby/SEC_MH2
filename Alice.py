import time
import Utility
import socket
import ssl

# Client to Bob
def client_program():
    hostname='example.org'
    host = socket.gethostname()
    port = 5001
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    context.load_verify_locations('bobCert.pem')
    context.load_cert_chain('aliceCert.pem', 'aliceKey.pem')

    client = socket.create_connection((host, port))
    tls = context.wrap_socket(client, server_hostname=hostname)

    # Establish TLS is configured correctly
    serverCertificate = tls.getpeercert()
    print(f"Does server have cert: {serverCertificate != None}")

    shake = tls.do_handshake()
    print(f"handshake done: {shake == None}")

    a, b, c = tls.cipher()
    print(f"TLS cipher: {a, b, c}")

    print("\n======== PROTOCOL BEGINS ========\n")
    while True:
        time.sleep(1)
        # Select random r for Alice
        aliceR = Utility.randBitStr(256)
        # Select random message
        aliceM = Utility.randDie()

        # Alice sends Com(r, m) to Bob
        aliceCom = Utility.Com(aliceR, aliceM)
        print("Sending commitment to Bob")
        time.sleep(1)
        tls.send(str(aliceCom).encode())

        # Receive Bobs dice result
        bobM = tls.recv(1024).decode()
        print("Dice result received from Bob: " + bobM)
        time.sleep(1)

        # Send r and m to Bob
        print("Sending r and m to Bob")
        time.sleep(1)
        tls.send((aliceR + "," + str(aliceM)).encode())

        # Calculate dice result
        print(f"---- Virtual dice is: {Utility.dieCalc(bobM, aliceM)}\n")
        time.sleep(1)

    client.close()


if __name__ == '__main__':
    client_program()