<h1>App Description and Preview</h1>

<h1>Dependencies and Installation</h1>

<h2>Dependencies &nbsp;
    <a href="https://pypi.org/project/vectorbt" alt="Python Versions">
        <img src="https://img.shields.io/pypi/pyversions/vectorbt.svg?logo=python&logoColor=white">
    </a>
</h2>

<ol>
    <li>it's assumed that you already have a compatible version of Python (listed above) and ideally a new virtual environment</li>
    <li>original TA-Lib library</li>
    <li>libraries in requirements.txt</li>
    <li>mod_wsgi (only if web hosting the app)</li>
</ol>

TA-Lib requires more work than a pip install if you want to reproduce the project. This is because the TA-Lib Python library serves only as a compatibility layer for the original TA-Lib library which must be installed before running `pip install ta-lib`. For Linux, I've provided the steps below. For Mac, a similar procedure can be followed: 
<a href="https://medium.com/@mkstz/install-ta-lib-without-homebrew-61f57a63c06d">
    Installing TA-Lib without Homebrew
</a>

<h2>Ta-Lib Installation for Linux:</h2>

Install *wget* if you don't already have it, using the appropriate 
<a href="https://www.maketecheasier.com/install-software-in-various-linux-distros/">
    install command
</a> 
for your Linux distro. **For Debian/Ubuntu:**

```shell
sudo apt-get install wget
```

Download the TA-Lib library from 
<a href="https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/">
    SourceForge
</a>

```shell
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
```

Unpack the tar file

```shell
tar -xvf ta-lib-0.4.0-src.tar.gz
```

Delete the tar file, cd into the new folder, and run the configure file inside

```
rm ta-lib-0.4.0-src.tar.gz; cd ta-lib; ./configure --prefix=/usr
```

Run the `make` command to compile the TA-Lib files.\
Now run `sudo make install`, which will copy the compiled files into */usr/include/ta-lib*.

You should now be able to install vectorbt and all dependencies without any issues

```shell
pip3 install -r requirements.txt
```
If this generates errors about ta-lib then confirm that your Linux distro stores header files in a subdirectory of /usr. If not, change `./configure --prefix=/appropriate_directory` in the earlier step.

<h2>Web Hosting on an Apache Server using WSGI:</h2>

This section assumes you already have an Apache server setup and linked to a domain name.

Even with Apache installed, you may be missing important files for mod_wsgi. For Debian/Ubuntu run:

```shell
sudo apt-get install apache2-dev
```

If you've done `pip install mod-wsgi` already then locate your WSGI files with

```shell
mod_wsgi-express module-config
```

and copy the output. Now create a new mod load file in your Apache *mods-available* directory and paste that output inside it

```shell
vim /etc/apache2/mods-available/wsgi.load
```

*(If you're new to vim press `i` to insert text, paste like normal, press `escape`, then `:wq` to save changes and exit. If you make a mistake press `escape` then `:q!` to exit without saving changes or creating the new file.)*

Enable the new mod with `a2enmod wsgi`.

Now nagivate to the *.config* or *.htaccess* file (depending on your OS) that you have your virutal host information in. You'll need to add a WSGIScriptAlias with the location of the *.wsgi* file for the app.

If you site is only using http, your virtual host info should look similar to the below. If you have your site in a different directory from /var/www/ then change the entire root directory appropriately.

```apache
<VirtualHost *:80>
    ServerName yoursite.com
    ServerAlias www.yoursite.com
    WSGIScriptAlias / /var/www/yoursites_folder/dashapp/app.wsgi
    
    <Directory /var/www/yoursites_folder/dashapp/>
        Order allow,deny
        Allow from all
    </Directory>
</VirtualHost>
```

If your site has been setup to use https via Let's Encrypt then your .htaccess or .config file should look something like 

```apache
<VirtualHost *:80>
    ServerName yoursite.com
    ServerAlias www.yoursite.com

    RewriteEngine on
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://yoursite.com/$1 [L,R=301]
</VirtualHost>

<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName yoursite.com
    ServerAlias www.yoursite.com
    WSGIScriptAlias / /var/www/yoursites_folder/dashapp/app.wsgi

    <Directory /var/www/yoursites_folder/dashapp/>
        Order allow,deny
        Allow from all
    </Directory>
    
    Include /etc/letsencrypt/options-ssl-apache.conf
    SSLCertificateFile /etc/letsencrypt/live/yoursite.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yoursite.com/privkey.pem
</VirtualHost>
</IfModule>
```

If you've created a new *.config* or *.htaccess* file in one of your *...-available* folders rather than adding to an existing file then you'll also need to activate it with the appropriate `a2ensite`, `a2enmod`, or `a2enconf` command.

Finally, you will also need to edit the *app.wsgi* file from this repository by changing the sys.path line to the appropriate directory for your app

```python
sys.path.insert(0,"/var/www/yoursites_folder/dashapp/")
```

Now restart Apache `systemctl restart apache2` for all changes to take effect. The app should now be accessible through your domain name 🤩.
