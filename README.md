# udacity_P5
*************************
Project P5 readme.md file
*************************

1. GitHub repo link:
--------------------
https://github.com/bahobab/udacity_P5

2. Readme.md contents:
----------------------

i. The server can be accessed at:
	- ip address: 52.26.132.107
	- port: 2200

ii. url to the website:
	http://52.26.132.107

iii. A summary of software you installed and configuration changes made.

This section is divided in 2 parts:

The first is a list of modules installed on the server for the application to run successfully.
The list of the modules is the file requirements.txt

The second part is the main part of this readme file and has 3 main parts:

1. Setting up the virtual machine:
==================================

This part lists the steps listed in the "Project Details" section of the project to setup the virtual machine and install and configure the Flask web application that serves mod_wsgi and apache

2. Running the application:
===========================

This part presents the necessary changes that are made to the original P3 files to adapt them to run in the P5 server environment

3. Project Requirements:
========================

This part goes over the different project requirements that makes it easy for the grader to evaluate the project
It also shows how "EXCEED EXPECTATIONS" tasks are accomplished

iv. Third-party resources:

https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04
https://www.howtoforge.com/tutorial/ufw-uncomplicated-firewall-on-ubuntu-15-04/
https://www.digitalocean.com/community/tutorials/how-to-protect-ssh-with-fail2ban-on-ubuntu-14-04
https://www.digitalocean.com/community/tutorials/how-to-run-django-with-mod_wsgi-and-apache-with-a-virtualenv-python-environment-on-a-debian-vps
https://help.ubuntu.com/lts/serverguide/automatic-updates.html
http://askubuntu.com/questions/218259/how-to-change-the-email-interval-for-apticron
http://www.sysadminworld.com/2012/how-to-run-apticron-only-once-a-week/
http://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/
http://askubuntu.com/questions/8923/apticron-email-setting-format-for-multiple-recipients
https://help.ubuntu.com/lts/serverguide/user-management.html
http://xmodulo.com/set-password-policy-linux.html
http://codingtips.kanishkkunal.in/server-monitoring-program/
http://linux.die.net/man/1/monit
http://askubuntu.com/questions/122330/unable-to-restart-apache-getting-error-apache2-bad-user-name-apache-run-use
http://www.stuartellis.eu/articles/postgresql-setup/
https://www.howtoforge.com/tutorial/install-git-and-github-on-ubuntu-14.04/
http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/


=================================
A. SETTING UP THE VIRTUAL MACHINE
=================================

1/ Launch the VM per the instructions provided here:
https://www.udacity.com/account#!/development_environment or check out the file:
dev_environment.txt

2/ ssh to server:
follow the instructionns provided in the link above to ssh to the developement machine

In my case, I open a git bash shell and run the comand:

$ ssh -i ~/.ssh/udacity_key.rsa root@52.26.132.107
at this point I am root

3/ Create a new user: grader

# adduser grader
 
Follow the prompts to complete the new user creation

4/ Give grader the permission to sudo

# mkdir /etc/sudoers.d (if not already exists)
# nano /etc/sudoers.d/grader

>> add these contents to the grader file, then save and exit nano:
grader    ALL=(ALL) NOPASSWD:ALL

5/ Update currently installed packages
>> run these commands:

# apt-get update
# apt-get upgrade

6/ Change ssh port from 22 to 2200
>> edit sshd_config:

# nano /etc/ssh/sshd_config

in the file change the line:

Port 22

to:

port 2200

save and exit

** Warning: It's advised to log in to another terminal as root thru port 22 so that you do not log yourself out.

restart ssh service for the new port number to take effect:
# reload ssh

loging as grader from another git bash terminal window (this is a password-based login. Later we will disable this option and only enable and enforce rsa key login)

$ ssh -p2200 grader@52.32.132.107

NOTES:
At this point, while successfully logged in as grader the remaining tasks will be carried out out as grader using sudo permissions.

To configure ssh to:

- disable remote login for root
- disable password authentication
- enable/enforce rsa key authentication

please see PROJECT REQUIREMENTS section below for how to complete these tasks.

So from my git bash terminal window I can login as grader like so:

$ ssh -i ~/.ssh/udacity_key.rsa grader@52.26.132.107

the teminal command prompt will look like this:

grader@ip-10-20-39-26:~$

But I will use the short-hand $ to describe the commands

7/ configure ufw
----------------
check ufw statu:
$ sudo ufw status

set initial ufw rules:

$ sudo ufw default deny incoming
$ sudo ufw default allow outgoing
$ sudo ufw allow ntp
$ sudo ufw allow www
$ sudo ufw allow 2200
$ sudo ufw deny 22

8/ Configure local time zone to UTC
-----------------------------------
The server is already configured to UTC. Otherwise do the following:

$ sudo nano /etc/default/rcS

>> set the line:
UTC=yes

9/Install configure Apache to serve a Python mod_wsgi application
-----------------------------------------------------------------

$ sudo apt-get install apache2 libapache2-mod-wsgi

10/ Install configure and PostgreSQL
------------------------------------

$ sudo apt-get install postgresql

a)- do not allow remote connections to postgresql:

>> edit this file:

$ nano /etc/postgresql/9.3/main/postgresql.conf

>> Then replace:

listen_addresses='*'

with:

listen_addresses='localhost'

b)- create a new user (role) called catalog with limited permissions on the catalog database

>> create a user called catalog (initially, I set the password to be catalogue)

$ sudo adduser catalog

>> create a postgresql user (role) called catalog with these options:

$ sudo -u postgres createuser catalog -A -D

c)- create a database owned by user catalog with limited permissions.
The dabase name is catalog

$ sudo -u postgres createdb -O catalog catalog

d)- Connect to the database to verify it's been successfully created

$ sudo -u postgres psql

postgres=# \c catalog
You are now connected to database "catalog" as user "postgres".

catalog=# \du
                             List of roles
 Role name |                   Attributes                   | Member of
-----------+------------------------------------------------+-----------
 catalog   |                                                | {}
 postgres  | Superuser, Create role, Create DB, Replication | {}

>> Quit posqgres command shell

catalog=# \q

e)- configure postgresql client authentication:

$ sudo nano /etc/postgresql/9.3/main/pg_hba.conf

>> change:

# IPv4 local connections:
host all all 127.0.0.1/32 md5

to:

host all all 127.0.0.1/32 trust

11/ Install git, clone P3 repo, configure and serve a Python mod_wsgi application
---------------------------------

$ sudo apt-get install git

a)- clone P3

I created a special folder called ~/my_git where I host my cloned repos

$ cd ~/my_git
$ git clone https://github.com/bahobab/udacity_project3

This is the easiest way to clone a repo, rather than using the ssh method which will require an rsa key being installed

b)- Protect .git from browser access
create/edit .htaccess file in ./git folder

$ nano ~/my_git/catalog/.git/.htaccess

>> add these lines
Order allow,deny
Deny from all

c)- Configure and serve a Python mod_wsgi application:

At this point the development server is ready so that we can configure and run the web application.
I will use these tutorials to deploy and run a Flask catalog application in a virtual environment.

The tutorials can be found here:
http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/
https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps

>> Install pip package installer:

$ sudo apt-get install python-pip

>> Install virtualenv

$ sudo apt-get install virtualenv

i/- create the following directories that will host the flask application in a virtual environmnent:

$ sudo mkdir /var/www/catalog
$ sudo mkdir /var/www/catalog/catalog (this is the catalog application directory)

There are 2 more folders:

templates,
static
(/var/www/catalog/catalog/templates, /var/www/catalog/catalog/static) 

that already exist in the cloned repo from P3 so they do not need to be created

ii/- Now copy the git repos for P3 to the application directory

$ sudo cp ~/my_git/* /var/www/catalog/catalog

- rename application.py to __init__.py

$ mv /var/www/catalog/catalog/application.py /var/www/catalog/catalog/__init__.py

iii/- create the website configuration files for the application:

a) First, create the virtualhost configuration file:

$ sudo nano /etc/apache2/sites-enabled/catalog.conf

>> add these contents:

<VirtualHost *:80>
                ServerName 52.26.132.107
                ServerAdmin grader@localhost
                WSGIScriptAlias / /var/www/catalog/catalogapp.wsgi
                <Directory /var/www/catalog/catalog/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/catalog/catalog/static
                <Directory /var/www/catalog/catalog/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

Save and exit

b) Then the wsgi file:

$ sudo nano /var/www/catalog/catalogapp.wsgi

>> add these contents:

#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/")

from catalog import app as application
application.secret_key = '\x97\x97&i\x1a\xa36\xbe\x91\xdd\xa6\x01\x88\x18\xfe\xb9\xd9\xbe&\xdeN\x9c-'

######################################################################################
# if needed use the following 2 lines to generate the secret key from a Python console
# import os
# s_key = os.urandom(24)
######################################################################################

Save and exit

After that the directory structure for the app looks like this:

/var/www/catalog
/var/www/catalog/catalog
/var/www/catalog/catalog/templates
/var/www/catalog/catalog/static 

iv/- Move to the application directory and create a virtual environment

$ cd /var/www/catalog/catalog

v/- Create a virtual environment for the catalog application to run in a virtual environmment

$ sudo virtualenv catalogvenv

vi/- Activate the catalog virtual environment

$ source catalogvenv/bin/activate

The new prompt now is:
(catalogvenv)grader@ip-10-20-39-26:/var/www/catalog/catalog$

vii/- install modules for catalog app environment

apt-get install python-psycopg2
sudo pip install flask
sudo pip install oauth2client
sudo pip install flask.ext
sudo pip install Flask-SeaSurf
sudo pip install bleach
sudo pip install WTForms
sudo pip install Flask-WTF
sudo pip install SQLAlchemy
sudo pip install httplib2
sudo pip install urllib2
sudo pip install psycopg2
...
(I may have missed to list all the packages here)
See the package-requirements.txt for all packages/modules installed on the virtual environment are listed in the package_requirements.txt file

viii/- Enable the virtualhost:

$ sudo a2ensite

The final directory structure for the application looks like this:

|/var/www/catalog/
|----------------/catalog/
|-----------------------/static/
|-----------------------/templates/
|-----------------------(catalogvenv)
|-----------------------/__init__.py
|----------------/catalogapp.wsgi

Restart apache2:

$ sudo apachectl restart

==========================
B. RUNNING THE APPLICATION
==========================

1/ In order to be able to run the web application we need to update the JavaScript Origin information from Google and Facebook application console websites (and eventually the client secrets and/or client id)

- update the credentials on google application console to set the Authorized JavaScript Origins to:
http://52.26.132.107
Save

- If you reset the client secret:
download the new JASON file and copy the contents into to this file:
/var/www/catalog/catalog/client_secrets.json
- If needed update the client Id in the login file:
/var/www/catalog/catalog/templates/login.html

- Update the Facebook app wesite settings from:

http://127.0.0.1:5000/

to:

http://52.26.132.107/

Save

-If reset the client secret
- download the new json_client file to the application folder
/var/www/catalog/catalog/fb_client_secrets.json
- If needed update the client Id in the file:
/var/www/catalog/catalog/templates/login.html

2/ Update the __init__.py file to the new development environment as the cloned files from P3 will have some discrepencies

- Edit the __init__.py
$ nano /var/www/catalog/catalog/__init__.py

- change line:
UPLOAD_FOLDER = '/static/img/'
to:
UPLOAD_FOLDER = '/var/www/catalog/catalog/static/img/'

- change line:
IMG_COVER_SRC = '/static/img/bookcover/'
to:
IMG_COVER_SRC = '/var/www/catalog/catalog/static/img/bookcover/'

- change line:
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
to:
CLIENT_ID = json.loads(
    open(r'/var/www/catalog/catalog/client_secrets.json', 'r').read())['web']['client_id']

- change line:
app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
to:
app_id = json.loads(open('/var/www/catalog/catalog/fb_client_secrets.json', 'r').read())[
        'web']['app_id']

- change line:
app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
to:
    app_secret = json.loads(
        open('/var/www/catalog/catalog/fb_client_secrets.json', 'r').read())['web']['app_secret']

- change line:
oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
to:
oauth_flow = flow_from_clientsecrets(r'/var/www/catalog/catalog/client_secrets.json', scope='')

3/ In order to be able to save book images and author images to the server, you must give write permissions to the folder:

/var/www/catalog/catalog/static/img

with the following commands:

$ sudo chgrp -R www-data static/img
$ sudo chmod -R g+w static/img 

At this point the application should be running as expected pointing the browser to:

http://52.26.132.107

=======================
C. PROJECT REQUIREMENTS
=======================
This section is a review of the accomplished tasks and show how the "EXCEED EXPECTATION" tasks are accomplished

1/ User management:
-------------------

a) Disable remote login as root:
$ sudo nano /etc/ssh/sshd_conf

>> enable the line:
PermitRootLogin no 

b) Remote user that can sudo:

Create grader file in sudoers.d directory

$ sudo nano /etc/sudoers.d/grader
 
>> add these contents

grader    ALL=(ALL) NOPASSWD:ALL

grader can log in remotely and has sudo permission

c) Passwords are set securely:

- strong password policy enforced by installing pam-cracklib

$ sudo apt-get install libpam-cracklib

Set password policy in /etc/pam.d/common-password file

$ sudo nano /etc/pam.d/common-password file

>> Edit this line like so: 

password  requisite  pam_cracklib.so retry=3 minlen=10 difok=3 ucredit=-2 lcredit=-2 dcredit=-1 ocredit=-1

- root password has been disabled

$ sudo passwd -l root

- grader password set to meet password policy set in /etc/pam.d/common-password

2/ Security:
------------

a) Key-based authentication enforced via settings in /etc/ssh.d/...
$ sudo nano /etc/ssh/sshd_conf

>> enable these lines:

RSAAuthentication yes
PubkeyAuthentication yes
PermitEmptyPasswords no

b) SSH is hosted on a non-default port 2200 in /etc/....
$ sudo nano /etc/ssh/sshd_conf

>> Change line:
Port 22

to:
Port 2200

c) Most recent updates are installed
$ sudo apt-get update
$ sudo apt-get ugrade

EXCEED EXPECTATION:
+++++++++++++++++++

- firewall has been configured to monitor repeat unsuccessful logins, ban attackers:

This is accomplished by installing and configuring the fail2ban module to monitor SSH.
I used this tutorial from Digital Ocean to accomplish this:
https://www.digitalocean.com/community/tutorials/how-to-protect-ssh-with-fail2ban-on-ubuntu-14-04

$ sudo apt-get install fail2ban iptables-persistent

configuration file: /etc/fail2ban/jail.local

>> enable these lines loke so:

destemail = root@localhost grader@localhost

sendername = Fail2Ban

mta = sendmail

action = %(action_mwl)s

[ssh]

enabled  = true
port     = 2200
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 6

c) Automated package updates:

I installed and configured apticron to warn root and grader of new packages updates available
I configured unattended-updates which is already installed to automatically install security updates only.

Security packages are automatically upgraded:
/etc/apt/apt.conf.d/50unattended-upgrades
cron settings file: /etc/apt/apt.conf.d/10periodic

apticron will check for updates daily. The admin will be notified and make the determination whether to install the updates or not.

$ sudo apt-get install apticron

configuration file: /etc/apticron/apticron.conf
cron settings file: /etc/cron.d/apticron

>> set notification to:
EMAIL="root@localhost grader@localhost"

3/ Aplication:
--------------

a) Web server configured to serve application:

b) Database configured to serve data

c) VM can be remotely logged on

EXCEED EXPECTATION:
+++++++++++++++++++

a) Monitor applications and...

This accomplished with the monit package installed and configured to moinitor apache2 and postgresql services.

$ sudo apt-get install monit

These services are monitored and restarted if they are stopped as configured below:
configuration file: /etc/monit/monitrc

$ sudo nano /etc/monit/monitrc

>> Set the MTA
set mailserver localhost

>> Set the monitored services as follow

#==================== my config ===============================================

##################### apache2 ################################################
check process apache2 with pidfile /run/apache2/apache2.pid
    alert grader@localhost
    start program = "/etc/init.d/apache2 start"
    stop program  = "/etc/init.d/apache2 stop"

##################### postgresql #############################################
check process postgresql with pidfile /run/postgresql/9.3-main.pid
    alert grader@localhost
    start program = "/etc/init.d/postgresql start"
    stop program  = "/etc/init.d/postgresql stop"

This tutorial was used to install and configure monit:
http://codingtips.kanishkkunal.in/server-monitoring-program/

============ end application configuration ====================================


============  start examples of notifications and monitoring status ===========

see the notification_status_examples.txt file
