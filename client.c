#include <stdio.h>
#include <string.h>

#include <openssl/err.h>
#include <openssl/ssl.h>

int main(void) {
 
  int ret = 0;

  SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());
  ret = SSL_CTX_load_verify_locations(ctx, "ca_01.crt", NULL);
  if (ret == 0) printf("Could not load ca file.\n");

  BIO *bio = BIO_new(BIO_s_connect());
  BIO_set_conn_hostname(bio, "127.0.0.1");
  BIO_set_conn_port(bio, "6520");

  SSL *ssl = SSL_new(ctx);
  SSL_set_bio(ssl, bio, bio);

  SSL_connect(ssl);

  const char *msg = "Hello World!\n";
  int msg_len = strlen(msg);

  SSL_write(ssl, msg, msg_len);

  SSL_shutdown(ssl);
  SSL_free(ssl);
}
