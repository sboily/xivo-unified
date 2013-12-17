from yapsy.PluginManager import PluginManager
import os
import tempfile
import shutil
import tarfile
import urllib2
import json

from flask import current_app, g
from app import db
from models import Plugins
import logging 

logging.basicConfig(level=logging.DEBUG)

plugin_manager = None
plugin_directory = None
app = None

def init_plugin_manager(directory, created_app):
    global plugin_manager
    global plugin_directory
    global app
    plugin_directory = directory
    app = created_app

    plugin_manager = PluginManager()
    plugin_manager.setPluginPlaces([plugin_directory])
    plugin_manager.setPluginInfoExtension('plugin')
    plugin_manager.collectPlugins()


def setup_plugins():
    for plugin_info in plugin_manager.getAllPlugins():
        plugin_info.plugin_object.setup(app)

def activate_plugins():
    for plugin_info in plugin_manager.getAllPlugins():
        plugin_manager.activatePluginByName(plugin_info.name)


def get_plugin_list():
    plugin_list = []
    for plugin_info in plugin_manager.getAllPlugins():
        if hasattr(g, 'server_id'):
            plugin = Plugins.query.filter(Plugins.organisation_id == g.user.organisation_id) \
                                  .filter(Plugins.server_id == g.server_id) \
                                  .filter(Plugins.name == plugin_info.name) \
                                  .first()
        else:
            plugin = Plugins.query.filter(Plugins.organisation_id == g.user.organisation_id) \
                                  .filter(Plugins.name == plugin_info.name) \
                                  .first()

        if plugin:
            if hasattr(plugin_info.plugin_object, 'activated'):
                plugin_info.plugin_object.activated(plugin_info.name)

            if plugin_info.details.get('Documentation', 'Parent') == 'organisation' and g.user.role >= 200:
                if hasattr(g, 'server_id'):
                    pass
                else:
                    info = {'name': plugin_info.details.get('Documentation', 'DisplayName'),
                            'url': plugin_info.plugin_object.plugin_endpoint(),
                            'module': plugin_info.name,
                            'parent': plugin_info.details.get('Documentation', 'Parent'),
                            'version': plugin_info.details.get('Documentation', 'Version'),
                           }
                    if plugin_info.details.has_option('Documentation', 'Dependance'):
                         info['dep'] = plugin_info.details.get('Documentation', 'Dependance')
                    plugin_list.append(info)

            if plugin_info.details.get('Documentation', 'Parent') == 'server':
                if hasattr(g, 'server_id'):
                    info = {'name': plugin_info.details.get('Documentation', 'DisplayName'),
                            'url': plugin_info.plugin_object.plugin_endpoint(),
                            'module': plugin_info.name,
                            'parent': plugin_info.details.get('Documentation', 'Parent'),
                            'version': plugin_info.details.get('Documentation', 'Version'),
                           }
                    plugin_list.append(info)

    return plugin_list


def remove_plugin(plugin_name):
    _deactivated_plugin(plugin_name)
    _remove_from_db(plugin_name)
    #_remove_files(plugin_name)
    _unload_plugin(plugin_name)

def _deactivated_plugin(plugin_name):
    plugin = plugin_manager.getPluginByName(plugin_name)
    if hasattr(plugin.plugin_object, 'deactivated'):
        plugin.plugin_object.deactivated(plugin.name)

def _remove_from_db(plugin_name):
    plugin = Plugins.query.filter(Plugins.name == plugin_name) \
                          .filter(Plugins.organisation_id == g.user_organisation.id) \
                          .first()
    if hasattr(g, 'server_id'):
        plugin = Plugins.query.filter(Plugins.name == plugin_name) \
                              .filter(Plugins.organisation_id == g.user_organisation.id) \
                              .filter(Plugins.server_id == g.server_id) \
                              .first()
    db.session.delete(plugin)
    db.session.commit()


def _remove_files(plugin_name):
    plugin_path = os.path.join(plugin_directory, plugin_name)
    shutil.rmtree(plugin_path)

def _unload_plugin(plugin_name):
    plugin = plugin_manager.getPluginByName(plugin_name)
    plugin_manager.removePluginFromCategory(plugin, 'Default')


def install_plugin(plugin_name):
    print "Installing plugin %s" % plugin_name
    _add_to_db(plugin_name)
    _download_and_extract(plugin_name)
    #_load_plugin(plugin_name)

def _add_to_db(plugin_name):
    plugin = Plugins(plugin_name)
    plugin.organisation_id = g.user.organisation_id
    if hasattr(g, 'server_id'):
        plugin.server_id = g.server_id
    db.session.add(plugin)
    db.session.commit()

def _download_and_extract(plugin_name):
    dst = plugin_directory

    src = tempfile.mkdtemp()
    url = "http://market.xivo.fr/%s.tgz" % plugin_name

    mod = urllib2.urlopen(url)
    mod_file = open(src + url.split('/')[-1], 'w')

    mod_file.write(mod.read())
    mod_file.close()
    mod.close()

    tar = tarfile.open(src + plugin_name + ".tgz")
    tar.extractall(path=dst)
    tar.close()

    shutil.rmtree(src)

def _load_plugin(plugin_name):
    plugin_manager.collectPlugins()
    plugin_manager.activatePluginByName(plugin_name)

    plugin = plugin_manager.getPluginByName(plugin_name)
    plugin.plugin_object.setup(current_app)
