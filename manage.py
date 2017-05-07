from src.app import app, db

from flask_script import Manager, Server as FlaskServer
from flask_migrate import Migrate, MigrateCommand
from src.app.models import *  # Don't remove this line, thinking it's a unused import
import config

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('run_test_server',
                    FlaskServer(host=config.TEST_SERVER_HOST, port=config.TEST_SERVER_PORT, threaded=True,
                                use_debugger=True, use_reloader=True))

if __name__ == "__main__":
    manager.run()
