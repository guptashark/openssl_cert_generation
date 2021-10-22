import subprocess

f = open("serial_ca", "w");
f.write("1000")
f.close()

f = open("serial_intermediate", "w");
f.write("1000")
f.close()

# Create the keys
subprocess.run(["openssl", "genrsa", "-out", "ca.key", "2048"])
subprocess.run(["openssl", "genrsa", "-out", "intermediate.key", "2048"])
subprocess.run(["openssl", "genrsa", "-out", "svr.key", "2048"])
subprocess.run(["openssl", "genrsa", "-out", "client.key", "2048"])

# Create the CA cert
subprocess.run(["openssl", "req", "-config", "ca_openssl.cnf",
    "-key", "ca.key", "-new", "-x509", "-days", "7300", "-sha256",
    "-extensions", "v3_ca", "-out", "ca.crt"])


# Create the intermediate csr.
subprocess.run(["openssl", "req", "-config", "intermediate_openssl.cnf",
    "-new", "-sha256",
    "-key", "intermediate.key",
    "-out", "intermediate.csr"])


# Sign the intermediate cert.
subprocess.run(["openssl", "x509", "-req",
    "-extfile", "intermediate_openssl.cnf",
    "-extensions", "v3_intermediate_ca",
    "-days", "3650",
    "-in", "intermediate.csr",
    "-CAkey", "ca.key",
    "-CA", "ca.crt", 
    "-CAserial", "serial_ca",
    "-out", "intermediate.crt"])

# Create the server csr.
subprocess.run(["openssl", "req", "-config", "server_openssl.cnf",
    "-key", "svr.key",
    "-new", "-sha256",
    "-out", "svr.csr"])

# Sign the server cert.
subprocess.run(["openssl", "x509", "-req",
    "-extfile", "server_openssl.cnf",
    "-extensions", "server_cert",
    "-days", "3000",
    "-in", "svr.csr",
    "-CAkey", "intermediate.key",
    "-CA", "intermediate.crt", 
    "-CAserial", "serial_intermediate",
    "-out", "svr.crt"])

# Create the client csr.
subprocess.run(["openssl", "req", "-config", "client_openssl.cnf",
    "-key", "client.key",
    "-new", "-sha256",
    "-out", "client.csr"])

# Sign the client cert.
subprocess.run(["openssl", "x509", "-req",
    "-extfile", "client_openssl.cnf",
    "-extensions", "usr_cert",
    "-days", "3000",
    "-in", "client.csr",
    "-CAkey", "intermediate.key",
    "-CA", "intermediate.crt", 
    "-CAserial", "serial_intermediate",
    "-out", "client.crt"])
