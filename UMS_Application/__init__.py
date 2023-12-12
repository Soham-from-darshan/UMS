from flask import Flask
import os

def make_app():
    # create app
    app = Flask(__name__, instance_relative_config=True)

    # provide some global variables that can be used anywhere with current_app.config[var_name]
    app.config.from_mapping(
        SECRET_KEY='ums', # this will be changed with a random token when deploying on server
        DATABASE=os.path.join(app.instance_path, 'ums.sqlite'), # db path
    )

    # create instance folder if its not there, this folder will contain database file that we will read/write  
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # created a sample route
    @app.route('/',methods=['GET'])
    def home():
        return 'Our sweet ums'

    return app

app = make_app()