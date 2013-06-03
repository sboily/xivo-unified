import os

def register_plugins(app):
    plugins_directory = os.path.join(app.config['BASEDIR'], 'app/plugins/')
    dirs = os.listdir(plugins_directory)
    plugins = []

    for directory in dirs:
        if os.path.isdir(os.path.join(plugins_directory,directory)):
            plugins.append(directory)

    return plugins

