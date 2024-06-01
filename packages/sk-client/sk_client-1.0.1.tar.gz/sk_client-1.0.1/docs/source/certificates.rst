Certificates
============

.. _certificates:

Certificate Support
-------------------
The SK-VPN supports Certificate Based Authentication.

The SK-VPN enforces algorithm compliance for internally generated and user uploaded Certificates. 

Certificates must meet the following standards:

* CNSA v1.0 Algorithms: `CNSA v1.0 <https://media.defense.gov/2021/Sep/27/2002862527/-1/-1/0/CNSS%20WORKSHEET.PDF>`_ 
* RSA (3072-bit+) 
* ECC (P-384+)
* Hashes (SHA-384+)


.. _cert_csr:

Certificate Signing Request (CSR)
---------------------------------

The SK-VPN supports generating Certificate Signing Requests (CSR) in order to generate 
private keys locally to the SK-VPN and generate a Certificate using a Certificate Authority (CA).

This process is used in mutliple scenarios including generating a Syslog client certificate
for Syslog authentication, and generating a HTTPS certificate for HTTPS authentication. 
The purpose of the CSR is to allow the user to sign the CSR which
can be used by Browsers, and other client software to authenticate the SK-VPN.


In order to generate a CSR, use the REST API:

* (*Pre*) Generate a Certificate Authority (CA) Root Certificate and Private Key pair which will be used to sign the Certificate
* Export a Certificate Signing Request: POST `/cert/signing-request`` 
  * Note the SK-VPN generates a Private Key and exports the CSR for the user to sign with the CA.
* Sign the CSR with the CA Root Private Key
* Upload the signed certificate to the SK-VPN via the POST `/cert/signed_csr`` endpoint with the `usage` field set to `SYSLOG_CLIENT`
* Verify the Certificate detials using the GET `/cert/syslog/client-cert`, `/cert/syslog/ca-cert` and `/cert/syslog/ca`
* Enable syslog authentication: POST `sys/syslog/settings` with the `enable_authentication` field set to True


.. _cert_details:

Certificate Information and Details
-----------------------------------
The SK-VPN provides information and details of all certificates on the system.
Certificate Information enpoints give a summary of the certificate and contains a Unique Identifier called the `fingerprint`
which is used in other Certificate Operations.
Certificate Details endpoints give the full description of the certificate and contains all fields in the certificate.

The REST API can be used to get the summary information of certificates:

* GET `/cert/certs`
* GET `/cert/ca`
* GET `/cert/user`

The REST API can be used to check the details of all certificates:

* GET `/cert/certs`
* GET `/cert/details`
* GET `/cert/tls/server-cert`
* GET `/cert/syslog/ca`
* GET `/cert/syslog/client-cert`

.. _cert_revocation_lists:

Certificate Revocation Lists
----------------------------

The SK-VPN does not support Certificate Revocation List (CRL) used to revoke certificates.
This feature will be added in a future update.

Currently the SK-VPN allows management of Certificates via the REST API, including deletion of Certificates.
IPsec Connections may be configured for re-authentication which does not require CRLs, but does enforce Certificate Date validation.


.. _cert_examples:

Example Certificate Operations
------------------------------

This section contains example OpenSSL commands that can be used to generate and sign certificates.

.. _ca_generation:

---------------------------------
Example CA Certificate Generation
---------------------------------

The below OpenSSL commands can be used to generate a self-signed (Root) Certificate Authority
which can be used to sign a Certificate Signing Request (CSR) for use by the SK-VPN.

.. code-block:: bash

    openssl req -x509 -newkey rsa:4096 -sha384 -days 3650 -keyout root_key.pem -out root_cert.pem -config openssl_root.conf

OpenSSL Configuration file (openssl_root.conf)

.. code-block:: bash
    
    ####################################################################
    [ ca ]
    default_ca    = CA_default      # The default ca section

    [ CA_default ]
    dir              = .
    certs            = $dir
    crl_dir          = $dir
    new_certs_dir    = $dir
    database         = $dir/syslog-root-ca-index.txt
    serial           = $dir/syslog-root-ca.srl

    default_days     = 3650         # How long to certify for
    default_crl_days = 30           # How long before next CRL
    default_md       = sha384       # Use public key default MD
    preserve         = no           # Keep passed DN ordering

    x509_extensions  = v3_ca        # The extensions to add to the cert

    email_in_dn     = no            # Don't concat the email in the DN
    copy_extensions = copy          # Required to copy SANs from CSR to cert

    policy            = signing_policy

    ####################################################################
    [ req ]
    default_bits       = 4096
    distinguished_name = ca_distinguished_name
    x509_extensions    = v3_ca
    string_mask        = utf8only

    ####################################################################
    [ ca_distinguished_name ]
    countryName         = Country Name (2 letter code)
    countryName_default = US

    stateOrProvinceName         = State or Province Name (full name)
    stateOrProvinceName_default = California


    organizationName            = Organization Name (eg, company)
    organizationName_default    = JET Technology Labs Inc

    commonName         = Common Name (e.g. server FQDN or YOUR name)
    commonName_default = TEST Root CA 1

    emailAddress         = Email Address
    emailAddress_default = info@jettechlabs.com

    ####################################################################
    [ v3_ca ]

    subjectKeyIdentifier   = hash
    authorityKeyIdentifier = keyid:always, issuer
    basicConstraints       = critical, CA:true
    keyUsage               = keyCertSign, cRLSign

    ####################################################################
    [ v3_intermediate_ca ]

    subjectKeyIdentifier   = hash
    authorityKeyIdentifier = keyid:always, issuer
    basicConstraints = critical, CA:true, pathlen:0
    keyUsage = critical, digitalSignature, keyCertSign, cRLSign
    extendedKeyUsage = serverAuth

    ####################################################################
    [ signing_policy ]
    countryName            = optional
    stateOrProvinceName    = optional
    localityName           = optional
    organizationName       = optional
    organizationalUnitName = optional
    commonName             = supplied
    emailAddress           = optional

    ####################################################################
    [ signing_req ]
    subjectKeyIdentifier   = hash
    authorityKeyIdentifier = keyid,issuer
    basicConstraints       = CA:FALSE
    keyUsage               = digitalSignature, keyEncipherment


.. _cert_generation:

------------------------------
Example Certificate Generation
------------------------------

The below OpenSSL (v3.0+) commands can be used to generate a Certificate Signing Request (CSR).

.. code-block:: bash

    # below adds subjectAltName to the CSR
    openssl req -new -nodes -sha384 \
    -subj "/CN=Test Certificate/O=Organization/ST=CA/C=US" \
    -extensions v3_req \
    -reqexts SAN \
    -key test_key.pem \
    -out test.csr \
    -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:10.10.10.1"))

.. _cert_signing:

---------------------------
Example Certificate Signing
---------------------------

A PEM formatted CSR file is exported from SK-VPN in most cases.
The below OpenSSL (v3.0+) commands can be used to sign the CSR using the CA Certificate and Private Key.

.. code-block:: bash

    # Sign the CSR using the CA certificate and Private Key
    openssl x509 -req -days 3650 -in test.csr \
    -CA root_cert.pem -CAkey root_key.pem \
    -CAcreateserial \
    -out test_cert.pem \
    -extfile <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:10.10.10.1")) \
    -extensions SAN