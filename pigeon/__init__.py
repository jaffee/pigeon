from flask import Flask
app = Flask(__name__, instance_relative_config=True)

try:
    app.config.from_envvar("PIGEON_CONFIG")
except RuntimeError:
    print "PIGEON_CONFIG environment variable not set. Using config.py"
    app.config.from_object("pigeon.config")


import pigeon.views
