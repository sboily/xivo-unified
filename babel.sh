# Init, to creating a new catalog (ex: french)
# pybabel extract -F babel.cfg -o messages.pot app
# pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot app
# pybabel init -i messages.pot -d app/translation -l fr


# Update 
# pybabel extract -F babel.cfg -o messages.pot app
# pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot app
# pybabel update -i messages.pot -d app/translations
# pybabel compile -d app/translations
# Edit the .pot file in the directory directly, with poedit for example
