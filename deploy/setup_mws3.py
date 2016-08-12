import subprocess

def subprocess_cmd(command):
    """
        Function used to run shell commands
        This is Python that creates a Python env
        which then runs Python commands - hhmmm
    """
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout



import MySQLdb as mdb
import sys
import os

filedir_path = "%s/.." % os.path.dirname(os.path.realpath(__file__))

# NOTE: A user could provide mangled strings to execute commands as the root mysql user
#   - but they have the root password anyway!!

#Test for root password
rootpass = raw_input("Root password for database:")

try:

    con = mdb.connect('localhost', 'root', rootpass, '');

except mdb.Error, e:
    print "Error - please check root database password"
    sys.exit(1)

finally:
    try:
        if con:
            cur = con.cursor()
            cur.execute("SELECT VERSION()")
            ver = cur.fetchone()
            print "Database version : %s " % ver

            con.close()
    except NameError:
        print " --Try again?-- "



print "The following settings can be edited later in the settings_mws3.py file:"
dbname=""
while (len(dbname) < 1 or len(dbname) > 9 ):
    dbname = raw_input("Please provide a name for your database: (max length: 9)")
dbname = "pc_%s" % dbname
password = raw_input("Enter a password your applicaton will use to access this database: ")
secret_key = raw_input("Enter a secret key for your application (this will be used by the application): ")
development = raw_input("Do you wish to load example data? [N]y: ")
is_dev=False
if development.lower() == "y":
    is_dev=True

username="%s_web" % dbname



try:
    con = mdb.connect('localhost', 'root', rootpass, 'test');
    cur = con.cursor()

    cur.execute("create database %s " % dbname)
    cur.execute("create user %s@'localhost' identified by '%s'" % (username,password) )
    cur.execute("grant all on %s.* to %s@'localhost'" % (dbname,username) )


except mdb.Error, e:

    print "****\nError we can not proceed:\n\n %d: %s \n****" % (e.args[0],e.args[1])
    sys.exit(1)

finally:

    #return the config strings

    f = open("%s/edpcmentoring/edpcmentoring/settings_mws3.py" % filedir_path, 'w')
    config = """
# This file has been generated using %s
from edpcmentoring.settings import *

SECRET_KEY='%s'
DEBUG = True
DATABASES = {
        'default' : {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '%s',
            'USER': '%s',
            'PASSWORD': '%s',
            'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
}""" % (sys.argv[0], secret_key, dbname, username, password)

    f.write( config )

    f.close()

    if con:
        con.close()


# we should now have a settings.mws3 file
#
# Next create the .htaccess file and place in the docroot
print "Generating the .htaccess file:  "
f = open("%s/../../docroot/.htaccess" % filedir_path,'w')
myhtaccess="""
AddHandler wsgi-script .py
Options FollowSymlinks ExecCGI MultiViews Indexes
MultiviewsMatch Handlers
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ wsgi.py/$1 [QSA,PT,L]
#Although this may set the variable - unabel to figure out how/when to retrieve it in the django project
#SetEnv DJANGO_SECRET_KEY 'some key goe shere'
"""
f.write(myhtaccess);
f.close()
print "done\n"

# Copy the wsgi.mws3 file from the edpcmentoring directory to the docroot
print "Copying mws3 specific wsgi.py file:   "
copycmd="cp %s/edpcmentoring/edpcmentoring/wsgi.py.mws3 %s/../../docroot/wsgi.py" % (filedir_path, filedir_path)
subprocess_cmd(copycmd);
print "done\n";

# install virtualenv into env dir
print "Generating the Python environment \n"
print "Virtual environment  "
virtcmd="virtualenv --system-site-packages -p/usr/bin/python2.7 %s/env" % filedir_path
subprocess_cmd(virtcmd)
print "done\n"

#install libraries
print "Installing Python libraries  "
installcmd=". %s/env/bin/activate; pip install -r %s/requirements_mws3.txt " % (filedir_path,filedir_path)
if is_dev:
   installcmd="%s -r %s/dev-requirements.txt" % (installcmd,filedir_path)
subprocess_cmd(installcmd);
print "done\n"

#create the database schema
print "Creating database tables"
schemacmd=". %s/env/bin/activate; %s/edpcmentoring/manage.py migrate  --settings=edpcmentoring.settings_mws3" % (filedir_path,filedir_path)
subprocess_cmd(schemacmd)
print "done\n"

if is_dev:
   # load the test data
   print "Load database with test data"
   datacmd=". %s/env/bin/activate; %s/edpcmentoring/manage.py runscript loadtestfixtures  --settings=edpcmentoring.settings_mws3 " % (filedir_path,filedir_path)
   subprocess_cmd(datacmd)
   print "done"

print "You should now be able to visit your web site! "



