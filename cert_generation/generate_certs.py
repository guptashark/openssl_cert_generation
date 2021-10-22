import subprocess

cert_structure = {}
cert_structure["ca"] = ["intermediate_01", "intermediate_02"]
cert_structure["intermediate_01"] = ["server_01", "client_01"]
cert_structure["intermediate_02"] = ["server_02", "client_02"]
cert_structure["server_01"] = []
cert_structure["server_02"] = []
cert_structure["client_01"] = []
cert_structure["client_02"] = []

def create_serial_files():
  for signer, signees in cert_structure.items():
    if len(signees) > 0:
      f = open("serial_" + signer, "w");
      f.write("1000")
      f.close()

def create_rsa_key(name):
  keyfile = name + ".key"
  subprocess.run(["openssl", "genrsa", "-out", keyfile, "2048"])

# Create the keys
def create_rsa_keys():
  for cert_name in cert_structure.keys():
    create_rsa_key(cert_name)

# Create the CA cert
def create_ca_cert():
  subprocess.run(["openssl", "req", "-config", "ca_openssl.cnf",
      "-key", "ca.key", "-new", "-x509", "-days", "7300", "-sha256",
      "-extensions", "v3_ca", "-out", "ca.crt"])

# Create a csr and sign it
def create_cert(ca_name, req_name):
  subprocess.run(["openssl", "req", "-config", req_name + ".cnf",
      "-new", "-sha256",
      "-key", req_name + ".key",
      "-out", req_name + ".csr"])

  subprocess.run(["openssl", "x509", "-req",
      "-extfile", req_name + ".cnf",
      "-extensions", "v3_" + req_name,
      "-days", "3650",
      "-in", req_name + ".csr",
      "-CAkey", ca_name + ".key",
      "-CA", ca_name + ".crt",
      "-CAserial", "serial_" + ca_name,
      "-out", req_name + ".crt"])

def create_certs():
  for signer, signees in cert_structure.items():
    if len(signees) > 0:
      for cert_name in signees:
        create_cert(signer, cert_name)

def verify_cert(ca_name, intermediate_name, leaf_name):
  subprocess.run(["openssl", "verify", "-verbose",
      "-CAfile", ca_name + ".crt",
      "-untrusted", intermediate_name + ".crt",
      leaf_name + ".crt"])

# Run the verification functions.
def verify_certs():
  verify_cert("ca", "intermediate_01", "server_01")
  verify_cert("ca", "intermediate_02", "server_02")

  verify_cert("ca", "intermediate_01", "client_01")
  verify_cert("ca", "intermediate_02", "client_02")


def generate_all():
  create_serial_files()
  create_rsa_keys()
  create_ca_cert()

  create_certs()

  verify_certs()

generate_all()
