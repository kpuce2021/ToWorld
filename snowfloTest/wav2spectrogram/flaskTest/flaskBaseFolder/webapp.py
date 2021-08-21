from flask import Flask, render_template, request, jsonify
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename
from functools import wraps
import sqlite3 as sql

from flask import Flask, g
from flask import Response, make_response

num = 0

def snowfloRes():
    custom_res = Response("snowfloResponse",200,{'saebom':'joa'})
                          # body에 실음           # header에 실음
    return custom_res

# =================================================================================
