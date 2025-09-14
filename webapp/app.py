# 從 flask 套件中匯入 Flask 網頁應用程式類別
from datetime import date, timedelta
from flask import Flask, render_template, send_from_directory
from flask import session, request, redirect, url_for, current_app
from functools import wraps
from webapp.amaindb import MAINDB
from webapp.modules import utils
from webapp.modules.locals import *
import json
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
print(SECRET_KEY)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
cyear = date.today().year
nowid = lambda: utils.get_nowid()
dtnow = lambda: utils.get_now()
# 以資料庫類別建構函式 MAINDB() 建立物件 mainDB
mainDB = MAINDB()
# 專案資料夾
print('app.root_path:', app.root_path)

@app.route('/')
def index():
    return "<h1>Hello, World!</h1>"
