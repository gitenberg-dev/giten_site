#!/bin/bash

curdate=$(date +"%Y-%m-%d")

# Make sure we've got the previous certificate
if [ ! -d /etc/letsencrypt ]; then
    echo "Existing certificate not found on server.  Pulling a backup copy from S3"
    aws s3 cp --recursive s3://lencrypt /etc/letsencrypt
else
    echo "Certificate already present locally"
fi

# Grab the modification time for the certificate
OLD_MOD_TIME=$(stat -c %Y /etc/letsencrypt/live/www.gitenberg.org/cert.pem)

# Download letsencrypt client
if [ -d /opt/letsencrypt/letsencrypt ]; then
    cd /opt/letsencrypt/letsencrypt
    git pull
else
    git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt/letsencrypt
    cd /opt/letsencrypt/letsencrypt
fi

PROJECT_DIR="/opt/python/current/app"

# This will renew the certificate
./letsencrypt-auto certonly --webroot -w "$PROJECT_DIR"/letsencrypt/ -d www.gitenberg.org -d gitenberg.org --debug --agree-tos --config /opt/letsencrypt/cli.ini

# Check that everything succeeded
if [ $? -ne 0 ]; then
    echo "An error occurred with the letsencrypt cert process."
else
    NEW_MOD_TIME=$(stat -c %Y /etc/letsencrypt/live/www.gitenberg.org/cert.pem)
    if [ "${OLD_MOD_TIME}" != "${NEW_MOD_TIME}" ]; then
        # Certificate file was modified, proceed
        echo "Successfully renewed the certificate.  Upload to AWS IAM."
        aws iam upload-server-certificate --server-certificate-name gitenberg-lencrypt-${curdate} --certificate-body file:///etc/letsencrypt/live/www.gitenberg.org/cert.pem --private-key file:///etc/letsencrypt/live/www.gitenberg.org/privkey.pem --certificate-chain file:///etc/letsencrypt/live/www.gitenberg.org/chain.pem | tee /tmp/aws_upload.response

        if [ $? -ne 0 ]; then
            echo "An error occurred uploading the certificate to AWS IAM"
        else
            cert_arn=$(grep 'Arn' /tmp/aws_upload.response | sed -e "s/^.*\"arn:/arn:/" -e "s/\",\s*$//")
            echo "Found ARN ${cert_arn} for uploaded certificate"
            # ARN contains a / character, so use alternate separators for sed command
            sed -e "s~REPLACEME~${cert_arn}~" /tmp/arn_options.json > /tmp/arn_options_${curdate}.json
            echo "Update environment configuration with the new certificate"
            aws elasticbeanstalk update-environment --environment-name giten-site-dev --option-settings file:///tmp/arn_options_${curdate}.json
            echo "Upload Certs to S3 for future reference"
            aws s3 cp --recursive /etc/letsencrypt s3://lencrypt/
        fi
    else
        echo "Certificate file not modified, but the process succeeded. Assuming no renewal happened."
    fi
fi

# Make *sure* we don't lose the logs in the event of instance restart
aws s3 cp /var/log/letsencrypt_renewal.log s3://lencrypt/letsencrypt_renewal.log-${curdate}

exit 0
