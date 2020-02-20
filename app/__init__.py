__author__ = 'Yash'

from flask import Flask
import os

SECRET_KEY = os.urandom(24)
SESSION_COOKIE_NAME = "IMAGE_RESIZE"

app = Flask(__name__)

app.config['UPLOADED_IMAGES_DEST'] = '/app/uploads'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_COOKIE_NAME'] = SESSION_COOKIE_NAME