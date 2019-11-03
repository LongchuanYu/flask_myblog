from flask_script import Server,Manager
from myapp import create_app
manager=Manager(create_app)
manager.add_command("runserver",Server(use_debugger=True))
if __name__=="__main__":
    manager.run()