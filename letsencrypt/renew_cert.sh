#!/bin/bash

if [ -d /opt/letsencrypt/letsencrypt ]; then
    cd /opt/letsencrypt/letsencrypt
    git pull
else
    git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt/letsencrypt
    cd /opt/letsencrypt/letsencrypt
fi

PROJECT_DIR="/opt/python/current/app"

./letsencrypt-auto certonly --webroot -w "$PROJECT_DIR"/letsencrypt/ -d www.gitenberg.org -d gitenberg.org --debug --agree-tos --config /opt/letsencrypt/cli.ini

# Check the return code
if [ $? -ne 0 ]; then
    echo "An error occurred with the letsencrypt cert process."
else
    echo "Successfully renewed the certificate.  Upload it to IAM."
    aws iam upload-server-certificate --server-certificate-name gitenberg-lencrypt --certificate-body file:///etc/letsencrypt/live/www.gitenberg.org/cert.pem --private-key file:///etc/letsencrypt/live/www.gitenberg.org/privkey.pem --certificate-chain file:///etc/letsencrypt/live/www.gitenberg.org/chain.pem
    echo "Upload Certs to S3."
    aws s3 cp --recursive /etc/letsencrypt s3://lencrypt/
fi

exit 0
