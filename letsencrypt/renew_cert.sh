#!/bin/bash

if [ -d /opt/letsencrypt/letsencrypt ]; then
    cd /opt/letsencrypt/letsencrypt
    git pull
else
    git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt/letsencrypt
    cd /opt/letsencrypt/letsencrypt
fi

PROJECT_DIR=$(cat prj_dir)

# TODO: Remove --dry-run to do it for real
./letsencrypt-auto --webroot -w "$PROJECT_DIR"/letsencrypt/ --renew -d www.gitenberg.org -d gitenberg.org --dry-run certonly

# Check the return code
if [ $? -ne 0 ]; then
    echo "An error occurred"
else
    echo "Success! Upload it."
    # aws iam upload-server-certificate --server-certificate-name gitenberg-both --certificate-body /etc/letsencrypt/live/www.gitenberg.org/cert.pem --private-key /etc/letsencrypt/live/www.gitenberg.org/privkey.pem --certificate-chain /etc/letsencrypt/live/www.gitenberg.org/chain.pem
fi
