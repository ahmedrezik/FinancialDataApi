from flask import Flask
from datetime import datetime
from flask import request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import yfinance as yf
import pandas as pd

app = Flask(__name__)







@app.route("/")
def home():
    return "Welcome to Stocks Backend"

@app.route("/getPrice",methods=['GET'])
def getData():
    requestBody = request.get_json(force=True)
    ticker = requestBody['tkr']
    tick = yf.Ticker(ticker)
    data = tick.history(period="1")
    return str(data['Open'].values[0])
  
@app.route("/getHistory",methods=['GET'])
def getHistory():
    requestBody = request.get_json(force=True)
    ticker = requestBody['tkr']
    tick = yf.Ticker(ticker)
    data = tick.history(period="max")
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    data.set_index("Date",inplace=True)
    return data['Close'].to_json(date_unit='ns')

if __name__ == "__main__":
    app.run(debug=True)