City-Digits
===========

MIT City Digits -- Module 2 on informal banking and alternative financial services


Development Environment
======================

    install virtualenv
    create virtualenv city_digits
    run python setup.py install


Inital Setup
============

    python manage.py syncdb
    python manage.py migrate city_digits
    mkdir media/backup
    python manage.py import_old_data



Production setup
================

    The production environment for this application is ghostmap.mit.edu. The home directory will be '/var/www/city_digits/' ($HOME_DIRECTORY). The installation
    directions below are specific to this production instance and may need to be altered for another server.

    2013_09_07 : Created ssh key-pair for client's github account
                    $ ssh-keygen -t rsa -C "sew.williams@gmail.com"

               : Added generated key-pair to client's github SSH Keys

               : created virtual environment directory at $HOME_DIRECTORY/.virtualenv

               : made virtual environment for project
                    $ virtualenv --no-site-packages city_digits

               : Checked out application from client's github to '$HOME_DIRECTORY/app/'
                    $ git clone git@github.com:NiJeLorg/City-Digits.git
					
               : Activate virtual environment and install app dependencies
                    $ source $HOME_DIRECTORY/.virtualenv/city_digits/bin/activate

               : Install needed mysql configs
                    $ sudo apt-get install libmysqlclient-dev python-dev
		
	       : Install needed PIL dependencies
                    $ sudo pip uninstall PIL
		    $ sudo apt-get install libjpeg-dev 
                    $ sudo apt-get install zlib1g-dev 
                    $ sudo apt-get install libpng12-dev 	    
		    $ sudo pip install PIL

               : install app dependencies
                    $ python setup.py install

               : install mod_wsgi for apache
                    $ sudo aptitude install libapache2-mod-python libapache2-mod-wsgi
	
	       : Turn on mod_expires and mod_headers
 		
               : create media directory and backup directory
                    $ mkdir media; mkdir media/backup ; chmod a+rw media

               : add project apache config (below)

               : install mysql (pw: citydigits)
                    $ sudo apt-get install mysql-server

               : secure mysql server (answer yes to all questions)
                    $ mysql_secure_installation

               : create database and project user (get username and password from client)
                    $ mysql -u root -p
                    mysql> create database city_digits;
                    mysql> grant all on city_digits.* to 'username' identified by 'password';

               : update settings.py with db user and password

               : set upstream repo (this will allow client to fetch updates from developers github)
                    $ git remote add upstream https://github.com/NiJeLorg/City-Digits.git

                : install dateutil.parser
                    $ sudo pip install python-dateutil --upgrade

               : do initial setup
                    $ python manage.py syncdb
                    $ python manage.py migrate city_digits
                    $ python manage.py import_old_data




Apache config
=============

    ##############################
    ## City Digits WSGI         ##
    ##############################

    Alias /favicon.ico /afs/athena.mit.edu/user/v/d/vdat/app/citi_digits/mit_civic/citi_digits/static/favicon.ico

    AliasMatch ^/([^/]*\.css) /afs/athena.mit.edu/user/v/d/vdat/app/citi_digits/mit_civic/citi_digits/static/css/$1

    Alias /media/  /afs/athena.mit.edu/user/v/d/vdat/app/citi_digits/mit_civic/media/
    Alias /static/ /afs/athena.mit.edu/user/v/d/vdat/app/citi_digits/mit_civic/citi_digits/static/

	<Directory /afs/athena.mit.edu/user/v/d/vdat/app/citi_digits/mit_civic/citi_digits/static>
	Order deny,allow
	Allow from all
	<IfModule mod_expires.c>
	  ExpiresActive On
	  ExpiresDefault "access plus 1 seconds"
	  ExpiresByType text/html "access plus 1 seconds"
	  ExpiresByType image/gif "access plus 10080 minutes"
	  ExpiresByType image/jpeg "access plus 10080 minutes"
	  ExpiresByType image/png "access plus 10080 minutes"
	  ExpiresByType text/css "access plus 60 minutes"
	  ExpiresByType text/javascript "access plus 60 minutes"
	  ExpiresByType application/x-javascript "access plus 60 minutes"
	  ExpiresByType text/xml "access plus 60 minutes"
	</IfModule>
	</Directory>
	
	<Directory /afs/athena.mit.edu/user/v/d/vdat/app/citi_digits/mit_civic/media>
	Order deny,allow
	Allow from all
	<IfModule mod_expires.c>
	  ExpiresActive On
	  ExpiresDefault "access plus 1 seconds"
	  ExpiresByType text/html "access plus 1 seconds"
	  ExpiresByType image/gif "access plus 10080 minutes"
	  ExpiresByType image/jpeg "access plus 10080 minutes"
	  ExpiresByType image/png "access plus 10080 minutes"
	  ExpiresByType text/css "access plus 60 minutes"
	  ExpiresByType text/javascript "access plus 60 minutes"
	  ExpiresByType application/x-javascript "access plus 60 minutes"
	  ExpiresByType text/xml "access plus 60 minutes"
	</IfModule>
	</Directory>
	
	WSGIScriptAlias /citydigits /afs/athena.mit.edu/user/v/d/vdat/app/citi_digits/mit_civic/mit_civic/wsgi.py
	WSGIPythonPath /afs/athena.mit.edu/user/v/d/vdat/app/citi_digits/mit_civic:/afs/athena.mit.edu/user/v/d/vdat/.virtualenv/city_digits/lib/python2.6/site-packages
	#WSGIPythonPath /afs/athena.mit.edu/user/v/d/vdat/app/citi_digits/mit_civic
	
	
	<Directory /afs/athena.mit.edu/user/v/d/vdat/app/citi_digits/mit_civic/mit_civic>
	<Files wsgi.py>
	Order deny,allow
	Allow from all
	</Files>
	<IfModule mod_expires.c>
	  ExpiresActive On
	  ExpiresDefault "access plus 1 seconds"
	  ExpiresByType text/html "access plus 1 seconds"
	  ExpiresByType image/gif "access plus 10080 minutes"
	  ExpiresByType image/jpeg "access plus 10080 minutes"
	  ExpiresByType image/png "access plus 10080 minutes"
	  ExpiresByType text/css "access plus 60 minutes"
	  ExpiresByType text/javascript "access plus 60 minutes"
	  ExpiresByType application/x-javascript "access plus 60 minutes"
	  ExpiresByType text/xml "access plus 60 minutes"
	</IfModule>
	</Directory>
	
