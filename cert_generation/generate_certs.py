import subprocess

def create_serial_files():
  f = open("serial_ca", "w");
  f.write("1000")
  f.close()

  f = open("serial_intermediate_01", "w");
  f.write("1000")
  f.close()

  f = open("serial_intermediate_02", "w");
  f.write("1000")
  f.close()

# Create the keys
def create_rsa_keys():
  subprocess.run(["openssl", "genrsa", "-out", "ca.key", "2048"])

  subprocess.run(["openssl", "genrsa", "-out", "intermediate_01.key", "2048"])
  subprocess.run(["openssl", "genrsa", "-out", "intermediate_02.key", "2048"])

  subprocess.run(["openssl", "genrsa", "-out", "server_01.key", "2048"])
  subprocess.run(["openssl", "genrsa", "-out", "server_02.key", "2048"])

  subprocess.run(["openssl", "genrsa", "-out", "client_01.key", "2048"])
  subprocess.run(["openssl", "genrsa", "-out", "client_02.key", "2048"])

# Create the CA cert
def create_ca_cert():
  subprocess.run(["openssl", "req", "-config", "ca_openssl.cnf",
      "-key", "ca.key", "-new", "-x509", "-days", "7300", "-sha256",
      "-extensions", "v3_ca", "-out", "ca.crt"])

# Create the intermediate_01 csr.
def create_intermediate_01_cert():
  subprocess.run(["openssl", "req", "-config", "intermediate_01.cnf",
      "-new", "-sha256",
      "-key", "intermediate_01.key",
      "-out", "intermediate_01.csr"])

  # Sign the intermediate_01 cert.
  subprocess.run(["openssl", "x509", "-req",
      "-extfile", "intermediate_01.cnf",
      "-extensions", "v3_intermediate_ca",
      "-days", "3650",
      "-in", "intermediate_01.csr",
      "-CAkey", "ca.key",
      "-CA", "ca.crt",
      "-CAserial", "serial_ca",
      "-out", "intermediate_01.crt"])

# Create the intermediate_02 csr.
def create_intermediate_02_cert():
  subprocess.run(["openssl", "req", "-config", "intermediate_02.cnf",
      "-new", "-sha256",
      "-key", "intermediate_02.key",
      "-out", "intermediate_02.csr"])

  # Sign the intermediate_02 cert.
  subprocess.run(["openssl", "x509", "-req",
      "-extfile", "intermediate_02.cnf",
      "-extensions", "v3_intermediate_ca",
      "-days", "3650",
      "-in", "intermediate_02.csr",
      "-CAkey", "ca.key",
      "-CA", "ca.crt",
      "-CAserial", "serial_ca",
      "-out", "intermediate_02.crt"])

# Create the server_01 csr.
def create_server_01_cert():
  subprocess.run(["openssl", "req", "-config", "server_01.cnf",
      "-key", "server_01.key",
      "-new", "-sha256",
      "-out", "server_01.csr"])

  # Sign the server_01 cert.
  subprocess.run(["openssl", "x509", "-req",
      "-extfile", "server_01.cnf",
      "-extensions", "server_cert",
      "-days", "3000",
      "-in", "server_01.csr",
      "-CAkey", "intermediate_01.key",
      "-CA", "intermediate_01.crt",
      "-CAserial", "serial_intermediate_01",
      "-out", "server_01.crt"])

# Create the server_02 csr.
def create_server_02_cert():
  subprocess.run(["openssl", "req", "-config", "server_02.cnf",
      "-key", "server_02.key",
      "-new", "-sha256",
      "-out", "server_02.csr"])

  # Sign the server_02 cert.
  subprocess.run(["openssl", "x509", "-req",
      "-extfile", "server_02.cnf",
      "-extensions", "server_cert",
      "-days", "3000",
      "-in", "server_02.csr",
      "-CAkey", "intermediate_02.key",
      "-CA", "intermediate_02.crt",
      "-CAserial", "serial_intermediate_02",
      "-out", "server_02.crt"])

# Create the client_01 csr.
def create_client_01_cert():
  subprocess.run(["openssl", "req", "-config", "client_01.cnf",
      "-key", "client_01.key",
      "-new", "-sha256",
      "-out", "client_01.csr"])

  # Sign the client_01 cert.
  subprocess.run(["openssl", "x509", "-req",
      "-extfile", "client_01.cnf",
      "-extensions", "usr_cert",
      "-days", "3000",
      "-in", "client_01.csr",
      "-CAkey", "intermediate_01.key",
      "-CA", "intermediate_01.crt",
      "-CAserial", "serial_intermediate_01",
      "-out", "client_01.crt"])

# Create the client_02 csr.
def create_client_02_cert():
  subprocess.run(["openssl", "req", "-config", "client_02.cnf",
      "-key", "client_02.key",
      "-new", "-sha256",
      "-out", "client_02.csr"])

  # Sign the client_02 cert.
  subprocess.run(["openssl", "x509", "-req",
      "-extfile", "client_02.cnf",
      "-extensions", "usr_cert",
      "-days", "3000",
      "-in", "client_02.csr",
      "-CAkey", "intermediate_02.key",
      "-CA", "intermediate_02.crt",
      "-CAserial", "serial_intermediate_02",
      "-out", "client_02.crt"])

# Run the verification functions.
def verify_certs():
  subprocess.run(["openssl", "verify", "-verbose",
      "-CAfile", "ca.crt",
      "-untrusted", "intermediate_01.crt",
      "server_01.crt"])

  subprocess.run(["openssl", "verify", "-verbose",
      "-CAfile", "ca.crt",
      "-untrusted", "intermediate_02.crt",
      "server_02.crt"])

  subprocess.run(["openssl", "verify", "-verbose",
      "-CAfile", "ca.crt",
      "-untrusted", "intermediate_01.crt",
      "client_01.crt"])

  subprocess.run(["openssl", "verify", "-verbose",
      "-CAfile", "ca.crt",
      "-untrusted", "intermediate_02.crt",
      "client_02.crt"])


create_serial_files()
create_rsa_keys()
create_ca_cert()
create_intermediate_01_cert()
create_intermediate_02_cert()
create_server_01_cert()
create_server_02_cert()
create_client_01_cert()
create_client_02_cert()
verify_certs()
