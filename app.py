# app.py - سیستم مدیریت هوشمند هزینه‌ها
from flask import Flask, request, jsonify, render_template_string
import json
import sqlite3
import os
import re
import requests
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = '''

