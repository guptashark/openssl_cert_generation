#include <stdio.h>
#include <string.h>

#include <openssl/err.h>
#include <openssl/ssl.h>

void dump_ssl_errs_v_01(void);
void dump_ssl_errs_v_02(void);

int ssl_verify_cb_01(int preverify_ok, X509_STORE_CTX *x509_ctx);

int main(void) {

  void (*dump_ssl_errs)(void) = dump_ssl_errs_v_02;

  // fn ptr to the verify callback.
  int (*ssl_verify_cb)(int preverify_ok, X509_STORE_CTX *x509_ctx);
  ssl_verify_cb = NULL;
 
  int ret = 0;
  (void)ret;

  SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());

  X509_STORE *x509_store = SSL_CTX_get_cert_store(ctx);

  X509_STORE_load_locations(x509_store, "cert_generation/ca_chain.crt", NULL);

  SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, ssl_verify_cb);

  BIO *bio = BIO_new(BIO_s_connect());
  BIO_set_conn_hostname(bio, "127.0.0.1");
  BIO_set_conn_port(bio, "6520");

  SSL *ssl = SSL_new(ctx);
  SSL_set_bio(ssl, bio, bio);

  SSL_connect(ssl);
  long verify_err = SSL_get_verify_result(ssl);
  printf("verify error on SSL_connect: %lu\n", verify_err);
  dump_ssl_errs();

  const char *msg = "Hello World!! It's working with automated script!\n";
  int msg_len = strlen(msg);

  SSL_write(ssl, msg, msg_len);

  SSL_shutdown(ssl);
  SSL_free(ssl);
}

void dump_ssl_errs_v_01(void) {
  unsigned long err = 0;
  char err_buff[256] = {'\0'};
  do {
    err = ERR_get_error();
    ERR_error_string(err, err_buff);
    printf("%s\n", err_buff);
  } while (err != 0);
}

void dump_ssl_errs_v_02(void) {
  unsigned long err = 0;
  do {
    err = ERR_get_error();
    const char *lib_name = ERR_lib_error_string(err);
    const char *func_name = ERR_func_error_string(err);
    const char *reason = ERR_reason_error_string(err);

    printf("error:%.8lX:%s:%s:%s\n", err, lib_name, func_name, reason);
  } while (err != 0);
}

int ssl_verify_cb_01(int preverify_ok, X509_STORE_CTX *x509_ctx) {
  (void)preverify_ok;
  (void)x509_ctx;
  return 1;
}
