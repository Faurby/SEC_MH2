# SEC_MH2

This is meant to be a "simulation" between Alice and Bob. For showing the protocol in effect, it is not possible in the current implementation to interact yourself between the two nodes. Proper example output as been placed in the folder `output`.

SSL Certificates and keys generated with `openssl`

```cmd
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem -subj "/C=DK/ST=Denmark/O=ITU/CN=example.org/emailAddress=bob@itu.dk"
```

To run the program, please open two terminals and have python 3 installed.

In terminal one:

```cmd
python Bob.py
```

In terminal two:

```cmd
python Alice.py
```
