
# Repo contaning basic flask rest api structure


* sh install.sh (will setup env and make config)
* edit config.py according to your configuration
* there is manage.py
    * to run the server for dev/test, run the command: sh scripts/run.sh (it internally runs ___python manage.py run_test_server___ with required options)
    * to run the flask shell, run the command: python manage.py shell
    * for wsgi setup, their is a different application.wsgi file
* to setup your DB, run ___python manage.py db init___ && ___python manage.py db upgrade___
    * for subsequent changes that you make to model, use ___python manage.py db migrate___ and then ___python manage.py db upgrade___
    * more documentation can be found [here](https://flask-migrate.readthedocs.io/en/latest/)