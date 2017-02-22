# -*- coding: utf-8 -*-
import os
from flask import Flask, request
from . import convertors
from . import cros



app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
  return 'home'
  return app.send_static_file('index.html')


@app.route('/chinese2arabic/<number>')
@cros.crossdomain(origin='*')
def chinese2arabic(number):
  """
  Convert chinese numbers to arabic numbers, only integer supported.
  """
  strict = request.args.get('strict', False)
  try:
    arabic = convertors.chinese2arabic(number, strict)
    format = request.args.get('format', None)
    if format == 'json':
      return "{'number': %d}" % int(arabic)
    else:
      return str(arabic)
  except:
    return 'Conversion failed'
