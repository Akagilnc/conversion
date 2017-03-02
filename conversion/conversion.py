# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from . import convertors
from . import cros



app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    return 'home', 200
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
            return jsonify({'number': int(arabic)}), 200
            # return "{'number': %d}" % int(arabic), 200
        else:
            return str(arabic), 200
    except:
        return 'Conversion failed', 200


@app.route('/myip')
@cros.crossdomain(origin='*')
def getclientip():
    format = request.args.get('format', None)
    if format == 'json':
        return jsonify(ip=request.remote_addr), 200
    else:
        return request.remote_addr, 200

