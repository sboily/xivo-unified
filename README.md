XiVO unified
============

XiVO unified is a proof of concept for the futur of XiVO and vision of the telephony in entreprise.

Installation
------------

1. apt-get install python-virtualenv python-pip rabbitmq-server libpython-dev couchdb
2. virtualenv xivo-unified
3. source xivo-unified/bin/activate (activate the virtualenv)
4. pip install -r requirements.txt (install the dependences, go to the root of the sources)
5. python ./run.py run (launch the application)
6. python ./runcelery.py worker (launch the task process)

.. warning:: The DEBUG settings in conf.py need to be true for the moment because we using the reload system from flask in debug mode for the market.

Using nginx and supervisord
---------------------------

For configuration with nginx, please install uwsgi 1.9 min and supervisor

1. apt-get install supervisor nginx
2. apt-get install libc-dev gcc python-dev (to compile uwsgi you need)
3. pip install uwsgi

Copy sources into /usr/share/nginx/www/xivo-unified

1. cp <xivo_unified_sources> /usr/share/nginx/www/
2. chown www-data.www-data /usr/share/nginx/www/xivo-xivo-unified -R

Nginx

1. cd SOURCES/conf/nginx
2. cp xivo /etc/nginx/sites-available/
3. mkdir /etc/nginx/ssl
4. cp server* /etc/nginx/ssl
5. ln -s /etc/nginx/sites-available/xivo /etc/nginx/sites-enabled/xivo
6. service nginx restart

Supervisor

1. cd SOURCES/conf/supervisor
2. cp * /etc/supervisor/conf.d/
3. service supervisor stop
4. service supervisor start

Clean
-----

1. apt-get remove --purge libc-dev-bin libc6-dev linux-libc-dev gcc libexpat1-dev libssl-dev python-dev python2.7-dev zlib1g-dev libpython-dev

Patch
-----

You need to patch PluginManager.py in yapsy.

Line 483 : candidate_module = imp.load_module('app.plugins.' + plugin_info.name,None,candidate_filepath,("py","r",imp.PKG_DIRECTORY))
