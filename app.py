from flask import Flask
from flask_cors import CORS, cross_origin
import logging

# DEBUGGER FOR WEG GUI
logging.basicConfig(filename='Logs/ErrorLogs.txt', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# ADD TEMPLATE FOLDER FOR STATIC PAGES
app = Flask(__name__, template_folder='GUI')
CORS(app)
