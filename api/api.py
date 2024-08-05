from flask import Flask
from scrape_and_process.price_predict import predict_price_over_time
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import os

scheduler = BackgroundScheduler()
csv_path = "shoe_data.csv"

#Daily csv updater
def update_csv():
    predict_price_over_time(True, csv_path)
    print("CSV updated")


def run_csv_updater():
    scheduler.add_job(
        update_csv,
        'interval',
        days = 1
    )
    scheduler.start()



#flask app
app = Flask(__name__)

@app.route("/data", methods = ["GET"])
def send_shoe_data():
    try:
        df = pd.read_csv(csv_path)
        return df.to_json()
    except FileNotFoundError:
        return "No data currently available"
    except Exception as e:
        return "Internal error"
    

update_csv()
run_csv_updater()
