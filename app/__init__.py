from flask import Flask

app = Flask(__name__, instance_relative_config=True)

from app import views

app.config.from_object('config')

app.config.from_mapping(SECRET_KEY='f905fa91afe84294ea89da342c0b46b20fd133c5')
