#include <stdio.h>
#include <string.h>

#include <openssl/err.h>
#include <openssl/ssl.h>

int main(void) {
 
  int ret = 0;
  unsigned long err = 0;
  char err_buff[256] = {'\0'};

  SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());
  ret = SSL_CTX_load_verify_locations(ctx, "ca_bad_name.crt", NULL);
  if (ret == 0) {
    do {
      err = ERR_get_error();
      ERR_error_string(err, err_buff);
      printf("%s\n", err_buff);
    } while (err != 0);
  }

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
