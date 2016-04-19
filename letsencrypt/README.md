
# Let's Encrypt Renewal Process

The [Let's Encrypt](https://letsencrypt.org/) renewal process is
reasonably simple, though tricky to get right.  

## Basic renewal process

Because the Elastic Beanstalk service will randomly recreate the server from
scratch, we have to take some care not to rely on any ephemeral files on the
server.  The basic overall process is:

1. Download the previous certificate information from S3
1. Run the letsencrypt-auto script
1. If we got a new certificate, upload that to the AWS Identity and Access
Management (IAM) service with a new certificate name
1. Change the configuration of the running service to use that name
1. Upload the new certificate information to S3

## Detailed process

There are three files which were created for this process and the interesting
parts of each are:

1. .ebextensions/03_letsencrypt.config -- This will automatically create
directories and such necessary for the process to run.
  * packages > yum > mailx -- The mailx package is required to send an email when a certificate requires renewal
  * files > /var/log/letsencrypt_renewal.log -- This log will contain the output of the periodic renewal process.
  * files > /opt/elasticbeanstalk/tasks/\* -- These files contain a configuration which tells EB to include the log for this process in the logs visible through the AWS Management Console.
  * files > /tmp/arn_options.json -- This *should* be the set of environment configuration updates to make after we're done, but this process is currently broken
  * commands > \* The command section prepares the folder /opt/letsencrypt which is where all of the process will run.
  * container_commands -- The whole process:
    1. Copy the renew_cert.sh and cli.ini files to the working directory.
    1. Create a cronjob which will run (0 5 2 \* \*) on the 2nd of the month, every month at 5AM
    1. Install that cronjob

1. letsencrypt/cli.ini -- This is a basic configuration file for letsencrypt
(currently only defines the email address of the owner of the site)
1. letsencrypt/renew_cert.sh -- This periodically run to attempt a renewal of
the certificate.
  * Restore the last certificates from S3. Because EB does not retain anything between deployments, we must not rely on previous runs being present. Everything is stored in S3 each time. Also, S3 does not support symlinks which seem to be required for letsencrypt to run properly, so we must hack around this and restore the original symlinks after the data itself is restored.
  * Store the OLD_MOD_TIME of the cert for later comparison to see if any update happened (which will *not* happen if we try to renew too soon)
  * Then we run letsencrypt-auto with these arguments:
    * --webroot -- Use the [webroot](https://letsencrypt.readthedocs.org/en/latest/using.html#webroot) plugin method
    * -w "$PROJECT_DIR"/letsencrypt/ -- Use this webroot root directory.  A static path of "http://gitenberg.org/.well-known/acme-challenge/" --> letsencrypt/.well-known/acme-challenge/ *must* be configured.  Let's Encrypt will automatically create a file at this location for the verification challenge.
    * -d www.gitenberg.org -d gitenberg.org -- These are the domains to create certs for
    * --debug -- currently Amazon AMI linux is not fully supported (but works fine)
    * --agree-tos -- Agree to the TOS with no prompting
    * --non-interactive -- Really, please turn off the prompting
    * --keep-until-expiring -- If the cert doesn't need to be renewed, just succeed (again, with no prompt) but do nothing
    * --config /opt/letsencrypt/cli.ini -- Use the config file with an email address in it
  * If that succeeds, we check to see if the cert was actually updated and, if so, upload it as a new cert to IAM.  It is not possible to update a cert in place after it is already created, so this will create a new certificate.
  * BROKEN: If that succeeds, ideally we would update the configuration for this site to use it, but that seems to be a brittle process which will put the site into a non-recoverable state until it is restored from backup. For now, we disable this.
  * TEMPORARY: Until the above works, we will just send an email (requiring the mailx package specified above)
  * Finally, we upload the new cert to S3 taking special care to save the symlink information so that we may restore it later.
  * Finally, finally, copy the log file to S3 just in case the instance goes away before we can see it.

## Notes:

The 'mailx' package and email process *should* be temporary.  Right now, the
command to update environment configuration seems very brittle.  Any changes
seem to break the environment.  If that happens the only way to recover is to
go to the AWS admin console configuration and Load Configuration from a
previous, known good state.  Until that is worked out, the only way to finalize
this process is for someone to login and change the Configuration > Network
Tier > Load Balancing > SSL certificate ID setting after each renewal of the
certificate.  The certificate is named with the renewal date so it should be
easy to find the most recent one.

The verification challenge that gets something at an address
http://gitenberg.org/.well-known/acme-challenge/ will only work if the machine
running the process can change that address and there are no other running
instances to serve something else (or something non-existent).  Basically this
means that if we run with more than one server, the verification may only
intermittently work correctly.
