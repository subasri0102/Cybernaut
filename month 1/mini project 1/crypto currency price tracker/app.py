from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

CSV_FILE = r"C:\Users\subasri\Desktop\cryptocurrency price tracker\month 1\mini project 1\crypto_prices_final.csv"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chart-data")
def chart_data():
    if not os.path.exists(CSV_FILE):
        return jsonify([])

    df = pd.read_csv(CSV_FILE)

    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
