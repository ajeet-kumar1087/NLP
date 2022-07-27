from flask import Flask , render_template

application = Flask(__name__)

from app import routes

application.run(debug=True)